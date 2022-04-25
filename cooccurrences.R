Sys.setenv("CORPUS_REGISTRY" = "/Volumes/cwb_registry/mac_registry")
library(polmineR)

spoken_male <- partition("BNC", u_sex="male")
spoken_female <- partition("BNC", u_sex="female")

word <- "ball_SUBST"
male_co <- cooccurrences(spoken_male, query = paste("[lemma='", word, "']", sep=""), left = 8, right=8, method="chisquare", verbose=T, cqp=T, p_attribute="lemma")
female_co <- cooccurrences(spoken_female, query = paste("[lemma='", word, "']", sep=""), left = 8, right=8, method="chisquare", verbose=T, cqp=T, p_attribute="lemma")