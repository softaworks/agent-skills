# AI Writing Pattern Catalog

Source: [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) + practitioner extensions.

---

## CONTENT PATTERNS

### 1. Inflated Significance / Legacy Language
**Trigger words:** stands as, serves as, is a testament/reminder, pivotal moment, underscores, reflects broader, symbolizing its enduring, setting the stage for, marks a shift, evolving landscape, indelible mark, deeply rooted

**Before:** > The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain.

**After:** > The Statistical Institute of Catalonia was established in 1989 to collect regional statistics independently from Spain's national statistics office.

---

### 2. Notability Padding
**Trigger words:** independent coverage, local/regional/national media outlets, active social media presence

**Before:** > Her views have been cited in The New York Times, BBC, Financial Times. She maintains an active social media presence with over 500,000 followers.

**After:** > In a 2024 NYT interview, she argued AI regulation should focus on outcomes rather than methods.

---

### 3. Superficial -ing Analysis
**Trigger words:** highlighting..., underscoring..., symbolizing..., contributing to..., fostering..., showcasing..., reflecting...

**Before:** > The color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, reflecting the community's deep connection to the land.

**After:** > The architect chose blue, green, and gold to reference local bluebonnets and the Gulf coast.

---

### 4. Promotional / Brochure Language
**Trigger words:** boasts a, vibrant, rich (figurative), profound, nestled, in the heart of, groundbreaking, renowned, breathtaking, must-visit, stunning

**Before:** > Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with rich cultural heritage.

**After:** > Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 5. Vague Attributions / Weasel Words
**Trigger words:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources

**Before:** > Experts believe the Haolai River plays a crucial role in the regional ecosystem.

**After:** > The Haolai River supports several endemic fish species, per a 2019 Chinese Academy of Sciences survey.

---

### 6. Formulaic "Challenges and Future Prospects" Sections
**Trigger words:** Despite its..., faces challenges typical of, Despite these challenges, Future Outlook, Challenges and Legacy

**Before:** > Despite its industrial prosperity, Korattur faces challenges typical of urban areas. Despite these challenges, Korattur continues to thrive.

**After:** > Traffic congestion increased after 2015 when three IT parks opened. The city began a drainage project in 2022.

---

## LANGUAGE / GRAMMAR PATTERNS

### 7. AI Vocabulary Overuse
**High-frequency words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry, testament, underscore, valuable, vibrant

**Before:** > Additionally, an enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:** > Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 8. Copula Avoidance ("serves as" instead of "is")
**Trigger words:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Before:** > Gallery 825 serves as LAAA's exhibition space. The gallery features four spaces and boasts over 3,000 square feet.

**After:** > Gallery 825 is LAAA's exhibition space. It has four rooms totaling 3,000 square feet.

---

### 9. Negative Parallelisms
**Pattern:** "Not only X but Y", "It's not just about X, it's Y", "Not merely A, but B"

**Before:** > It's not just about the beat riding under the vocals; it's part of the aggression. It's not merely a song, it's a statement.

**After:** > The heavy beat amplifies the aggressive tone.

---

### 10. Rule of Three Overuse
**Pattern:** Forced triads — keynote sessions, panel discussions, and networking opportunities; innovation, inspiration, and industry insights.

**Before:** > The event features keynote sessions, panel discussions, and networking opportunities.

**After:** > The event includes talks and panels, with time for informal networking.

---

### 11. Elegant Variation (Synonym Cycling)
**Pattern:** protagonist → main character → central figure → hero (all same person, repetition-penalty artifact)

**Before:** > The protagonist faces challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:** > The protagonist faces many challenges but eventually triumphs and returns home.

---

### 12. False Ranges
**Pattern:** "from X to Y" where X and Y aren't on a meaningful spectrum

**Before:** > Our journey has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter.

**After:** > The book covers the Big Bang, star formation, and theories about dark matter.

---

## STYLE PATTERNS

### 13. Em Dash Overuse
**Pattern:** Em dashes (—) used more than humans naturally do, imitating "punchy" writing.

**Before:** > The term is promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe"—yet this mislabeling continues—in official documents.

**After:** > The term is promoted by Dutch institutions, not the people themselves. The mislabeling continues in official documents.

---

### 14. Mechanical Boldface
**Pattern:** Bolding every technical term or concept, not for emphasis but for visual structure.

**Before:** > It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and **Business Model Canvas (BMC)**.

**After:** > It blends OKRs, KPIs, and the Business Model Canvas.

---

### 15. Inline-Header Bullet Lists
**Pattern:** Bullets with "**Header:** Description" format — lists that should be prose.

**Before:**
```
- **User Experience:** The UX improved with a new interface.
- **Performance:** Speed increased through optimized algorithms.
- **Security:** Strengthened with end-to-end encryption.
```

**After:** > The update improves the interface, speeds load times, and adds end-to-end encryption.

---

### 16. Title Case in Headings
**Pattern:** Capitalizing All Main Words In Headings when only first word + proper nouns should be capitalized.

**Before:** > ## Strategic Negotiations And Global Partnerships

**After:** > ## Strategic negotiations and global partnerships

---

### 17. Emoji Decoration
**Pattern:** 🚀 **Launch:** ... 💡 **Insight:** ... ✅ **Next Steps:** ...

**After:** Strip emojis. Convert to plain prose or simple headings.

---

### 18. Curly Quotation Marks
**Pattern:** ChatGPT uses curly quotes ("...") instead of straight ("..."). Signals AI origin.

---

## COMMUNICATION PATTERNS

### 19. Chatbot Meta-Language Left In
**Trigger words:** I hope this helps, Of course!, Certainly!, Would you like me to, let me know, here is a...

**Before:** > Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand.

**After:** > The French Revolution began in 1789 when financial crisis and food shortages led to unrest.

---

### 20. Knowledge-Cutoff Disclaimers
**Trigger words:** as of [date], Up to my last training update, While specific details are limited, based on available information

**Before:** > While specific details about the founding are not extensively documented, it appears to have been established sometime in the 1990s.

**After:** > The company was founded in 1994, per its registration documents.

---

### 21. Sycophantic / Servile Tone
**Pattern:** "Great question!", "You're absolutely right!", "That's an excellent point"

**After:** Remove entirely. State the substance directly.

---

## FILLER AND HEDGING

### 22. Common Filler Phrases
| Before | After |
|--------|-------|
| In order to achieve this goal | To achieve this |
| Due to the fact that | Because |
| At this point in time | Now |
| In the event that | If |
| Has the ability to | Can |
| It is important to note that | (delete) |

---

### 23. Over-Hedging
**Before:** > It could potentially possibly be argued that the policy might have some effect.

**After:** > The policy may affect outcomes.

---

### 24. Generic Positive Conclusions
**Before:** > The future looks bright. Exciting times lie ahead as they journey toward excellence.

**After:** > The company plans to open two more locations next year.
