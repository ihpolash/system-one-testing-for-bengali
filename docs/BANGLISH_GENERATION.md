# How the AI-generated Banglish was produced

**The original prompts were not recorded.** The two prompts below are written afterwards as a reference for the kind of instruction involved. They are illustrations, not the prompts that were actually used, and results should not be attributed to their exact wording.

Process (from the author):
1. ChatGPT (Luna 6.1) generated a Banglish rendering of every Bengali sentence (935 sentences from SentNoB, MASSIVE and XNLI-bn).
2. Grok (4.7) and Claude (Sonnet 5.5) were used to correct those renderings, under the author's supervision and review. About 35% of the renderings were changed in the correction passes.
3. The author corrected the spelling of the Bengali source in 81 sentences before romanization.
4. No sentence was typed by a person from scratch.

## Illustrative generation prompt

> Write the following Bengali sentence the way a Bengali speaker would type it in Latin letters on a phone (Banglish). Use common informal spelling, no diacritics, keep English words in English, and keep the meaning unchanged. Output only the Banglish sentence.
>
> Sentence: `<Bengali sentence>`

## Illustrative correction prompt

> Here is a Bengali sentence and a Banglish rendering of it. Check that the Banglish keeps the meaning, uses natural informal spelling and does not contain Bengali script. If it needs changes, output the corrected Banglish; if not, output it unchanged.
>
> Bengali: `<Bengali sentence>`
> Banglish: `<Banglish rendering>`
