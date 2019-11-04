
validation_filtered <- validation %>%
  filter(!is.na(ltiFeatures)) %>%
  filter(!is.na(stiFeatures))


interest_topics$topic_name <- as.character(interest_topics$topic_name)
category <- vector(mode="character", length=1411)
for (i in 1:1411) {
  category[i] = strsplit(interest_topics[i,2], '/')[[1]][2]
} 
new_interest_topics <- cbind(interest_topics,category)

validation_filtered <- right_join(validation_filtered,new_interest_topics, by = "topic_id")

sums <- validation_filtered %>%
  group_by(userID,category) %>%
  # group_by(category) %>%
  summarise(lti = sum(ltiFeatures), sti = sum(stiFeatures))


categories <- sort(unique(new_table$a))



sums_lti <- sums[1:3]
sums_sti <- sums[c(1,2,4)]

lti <- cast(sums_lti, userID~category)
sti <- cast(sums_sti, userID~category)

lti[is.na(lti)] <- 0
sti[is.na(sti)] <- 0

inAudience <- validation_filtered[1:2]
inAudience <- inAudience %>%
  group_by(userID) %>%
  distinct()

sti_2 <- left_join(sti, inAudience, by = "userID")
sti_2 <- sti_2[-which(sti_2$userID==0),]

lti_2 <- left_join(lti, inAudience, by = "userID")
lti_2 <- lti_2[-which(lti_2$userID==0),]

sti_2 <- sti_2 %>%
  mutate(inAudience = recode_factor(inAudience, "True" = 1, "False" = 0))

lti_2 <- lti_2 %>%
  mutate(inAudience = recode_factor(inAudience, "True" = 1, "False" = 0))

columns <- colnames(lti_2)
columns <- gsub(" & ", "_",columns)
columns <- gsub(" ", "_",columns)
colnames(lti_2) <- columns
colnames(sti_2) <- columns

write.csv(lti_2,"lti_valid.csv")
write.csv(sti_2,"sti_valid.csv")
