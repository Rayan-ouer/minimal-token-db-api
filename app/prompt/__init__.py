from app.prompt.prompts import sql_prompt, nlp_prompt

PROMPTS: dict[str, str] = {
    "sql_prompt": sql_prompt,
    "nlp_prompt": nlp_prompt,
}
