# Prompts

Each item is one typed single-choice question (`type: choice`) over a state. Dataset text appears only as `<field>`; option order is rotated by `BN_ROT` (0 here). Open models receive the same instructions, option names and descriptions through their own adapters (`harness/scripts/run_system_one_model.py`); Gemma scores each option label by next-token probability (`harness/jev_benchmarking/openmodel/prompts.py`).

## bn_sentnob

State fields: `comment`

```json
{
 "answer": {
  "type": "choice",
  "instructions": "What is the overall sentiment of `comment`?",
  "criteria": {
   "neutral": "The comment expresses no clear positive or negative opinion.",
   "positive": "The comment expresses a positive opinion or feeling.",
   "negative": "The comment expresses a negative opinion or feeling, including abuse."
  }
 }
}
```

## bn_bnli

State fields: `premise`, `hypothesis`

```json
{
 "answer": {
  "type": "choice",
  "instructions": "What is the relationship between `premise` and `hypothesis`?",
  "criteria": {
   "entailment": "`hypothesis` is definitely true given `premise`.",
   "neutral": "`hypothesis` may or may not be true; `premise` does not settle it.",
   "contradiction": "`hypothesis` is definitely false given `premise`."
  }
 }
}
```

## bn_massive

State fields: `utterance`

```json
{
 "answer": {
  "type": "choice",
  "instructions": "What does the user want the assistant to do with `utterance`?",
  "criteria": {
   "alarm_query": null,
   "alarm_remove": null,
   "alarm_set": null,
   "audio_volume_down": null,
   "audio_volume_mute": null,
   "audio_volume_other": null,
   "audio_volume_up": null,
   "calendar_query": null,
   "calendar_remove": null,
   "calendar_set": null,
   "cooking_query": null,
   "cooking_recipe": null,
   "datetime_convert": null,
   "datetime_query": null,
   "email_addcontact": null,
   "email_query": null,
   "email_querycontact": null,
   "email_sendemail": null,
   "general_greet": null,
   "general_joke": null,
   "general_quirky": null,
   "iot_cleaning": null,
   "iot_coffee": null,
   "iot_hue_lightchange": null,
   "iot_hue_lightdim": null,
   "iot_hue_lightoff": null,
   "iot_hue_lighton": null,
   "iot_hue_lightup": null,
   "iot_wemo_off": null,
   "iot_wemo_on": null,
   "lists_createoradd": null,
   "lists_query": null,
   "lists_remove": null,
   "music_dislikeness": null,
   "music_likeness": null,
   "music_query": null,
   "music_settings": null,
   "news_query": null,
   "play_audiobook": null,
   "play_game": null,
   "play_music": null,
   "play_podcasts": null,
   "play_radio": null,
   "qa_currency": null,
   "qa_definition": null,
   "qa_factoid": null,
   "qa_maths": null,
   "qa_stock": null,
   "recommendation_events": null,
   "recommendation_locations": null,
   "recommendation_movies": null,
   "social_post": null,
   "social_query": null,
   "takeaway_order": null,
   "takeaway_query": null,
   "transport_query": null,
   "transport_taxi": null,
   "transport_ticket": null,
   "transport_traffic": null,
   "weather_query": null
  }
 }
}
```

## bn_belebele

State fields: `passage`, `question`

```json
{
 "answer": {
  "type": "choice",
  "instructions": "Which option correctly answers `question` according to `passage`?",
  "criteria": {
   "A": "<answer option A>",
   "B": "<answer option B>",
   "C": "<answer option C>",
   "D": "<answer option D>"
  }
 }
}
```

## bn_sib200

State fields: `text`

```json
{
 "answer": {
  "type": "choice",
  "instructions": "What is the topic of `text`?",
  "criteria": {
   "science/technology": null,
   "travel": null,
   "politics": null,
   "sports": null,
   "health": null,
   "entertainment": null,
   "geography": null
  }
 }
}
```
