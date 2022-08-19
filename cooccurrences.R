Sys.setenv("CORPUS_REGISTRY" = "/Volumes/cwb_registry/mac_registry")
library(polmineR)

spoken_male <- partition("BNC", u_sex="male", p_attribute="lemma")
spoken_female <- partition("BNC", u_sex="female", p_attribute="lemma")

word <- "jammy_"
male_co <- cooccurrences(spoken_male, query = paste("[lemma='", word, "']", sep=""), left = 8, right=8, method="chisquare", verbose=T, cqp=T, p_attribute="lemma", boundary="s")
female_co <- cooccurrences(spoken_female, query = paste("[lemma='", word, "']", sep=""), left = 8, right=8, method="chisquare", verbose=T, cqp=T, p_attribute="lemma", boundary="s")

male <- as.data.frame(male_co)
female <- as.data.frame(female_co)

male <- male %>% subset(male$count_coi >= 5)
female <- female %>% subset(female$count_coi >= 5)

head(male)
head(female)

