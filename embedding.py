EMBDEDDING_MODEL_PATH = "/kaggle/input/qwen-3-embedding/transformers/0.6b/1"
MODEL_OUTPUT_PATH = '/kaggle/input/qwen3-0-6b-embedding-finetune-epoch2'
DATA_PATH = "/kaggle/input/jigsaw-agile-community-rules"

# https://huggingface.co/Qwen/Qwen3-Embedding-0.6B/blob/main/config_sentence_transformers.json
EMBEDDING_MODEL_QUERY = "Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:"

CLEAN_TEXT = True
TOP_K = 2000
BATCH_SIZE = 128

from cleantext import clean


def build_prompt(row):
    return f"""r/{row["subreddit"]}\nComment: {row["body"]}"""


def cleaner(text):
    return clean(text)


def get_dataframe_to_train(data_path):
    train_dataset = pd.read_csv(f"{data_path}/train.csv")
    test_dataset = pd.read_csv(f"{data_path}/test.csv")

    flatten = []
    flatten.append(train_dataset[["body", "rule", "subreddit", "rule_violation"]])

    for violation_type in ["positive", "negative"]:
        for i in range(1, 3):
            sub_dataset = test_dataset[[f"{violation_type}_example_{i}", "rule", "subreddit"]].copy()
            sub_dataset = sub_dataset.rename(columns={f"{violation_type}_example_{i}": "body"})
            sub_dataset["rule_violation"] = 1 if violation_type == "positive" else 0
            flatten.append(sub_dataset)

    dataframe = pd.concat(flatten, axis=0)
    dataframe = dataframe.drop_duplicates(ignore_index=True)
    return dataframe


def prepare_dataframe(dataframe):
    dataframe["prompt"] = dataframe.apply(build_prompt, axis=1)

    if CLEAN_TEXT:
        tqdm.pandas(desc="cleaner")
        dataframe["prompt"] = dataframe["prompt"].progress_apply(cleaner)

    if "rule_violation" in dataframe.columns:
        dataframe["rule_violation"] = dataframe["rule_violation"].map(
            {
                1: 1,
                0: -1,
            }
        )

    return dataframe


import pandas as pd
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search, dot_score
from tqdm.auto import tqdm
from peft import PeftModel, PeftConfig


def get_scores(test_dataframe):
    corpus_dataframe = get_dataframe_to_train(DATA_PATH)
    corpus_dataframe = prepare_dataframe(corpus_dataframe)

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(EMBDEDDING_MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(EMBDEDDING_MODEL_PATH)

    # Load adapter configuration and model
    adapter_config = PeftConfig.from_pretrained(MODEL_OUTPUT_PATH)
    lora_model = PeftModel.from_pretrained(model, MODEL_OUTPUT_PATH, config=adapter_config)
    merged_model = lora_model.merge_and_unload()
    tokenizer.save_pretrained("Qwen3Emb_Finetuned")
    merged_model.save_pretrained("Qwen3Emb_Finetuned")

    # 4. Tạo lại SentenceTransformer từ encoder đã merge
    embedding_model = SentenceTransformer(model_name_or_path="Qwen3Emb_Finetuned", device="cuda")

    print('Done loading model!')

    result = []
    for rule in tqdm(test_dataframe["rule"].unique(), desc=f"Generate scores for each rule"):
        test_dataframe_part = test_dataframe.query("rule == @rule").reset_index(drop=True)
        corpus_dataframe_part = corpus_dataframe.query("rule == @rule").reset_index(drop=True)
        corpus_dataframe_part = corpus_dataframe_part.reset_index(names="row_id")

        query_embeddings = embedding_model.encode(
            sentences=test_dataframe_part["prompt"].tolist(),
            prompt=EMBEDDING_MODEL_QUERY,
            batch_size=BATCH_SIZE,
            show_progress_bar=True,
            convert_to_tensor=True,
            device="cuda",
            normalize_embeddings=True,
        )
        document_embeddings = embedding_model.encode(
            sentences=corpus_dataframe_part["prompt"].tolist(),
            batch_size=BATCH_SIZE,
            show_progress_bar=True,
            convert_to_tensor=True,
            device="cuda",
            normalize_embeddings=True,
        )
        test_dataframe_part["semantic"] = semantic_search(
            query_embeddings,
            document_embeddings,
            top_k=TOP_K,
            score_function=dot_score,
        )

        def get_score(semantic):
            semantic = pd.DataFrame(semantic)
            semantic = semantic.merge(
                corpus_dataframe_part[["row_id", "rule_violation"]],
                how="left",
                left_on="corpus_id",
                right_on="row_id",
            )
            semantic["score"] = semantic["score"] * semantic["rule_violation"]
            return semantic["score"].sum()

        tqdm.pandas(desc=f"Add label for {rule=}")
        test_dataframe_part["rule_violation"] = test_dataframe_part["semantic"].progress_apply(get_score)
        result.append(test_dataframe_part[["row_id", "rule_violation"]].copy())

    submission = pd.concat(result, axis=0)
    return submission


def generate_submission():
    test_dataframe = pd.read_csv(f"{DATA_PATH}/test.csv")
    test_dataframe = prepare_dataframe(test_dataframe)

    submission = get_scores(test_dataframe)
    submission = test_dataframe[["row_id"]].merge(submission, on="row_id", how="left")
    submission.to_csv("submission_qwen3.csv", index=False)


if __name__ == "__main__":
    generate_submission()
