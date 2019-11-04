library(skimr)
library(tidyverse)
library(reshape)
validation <- read.csv("validation_tallskinny.csv")
training <- read.csv("training_tallskinny.csv")
interest_topics = read.csv("interest_topics.csv")

training_filtered <- training %>%
  filter(!is.na(ltiFeatures)) %>%
  filter(!is.na(stiFeatures))
validation_filtered <- validation %>%
  filter(!is.na(ltiFeatures)) %>%
  filter(!is.na(stiFeatures))

interest_topics$topic_name <- as.character(interest_topics$topic_name)
category <- vector(mode="character", length=1411)
for (i in 1:1411) {
  category[i] = strsplit(interest_topics[i,2], '/')[[1]][2]
} 
new_interest_topics <- cbind(interest_topics,category)

training_filtered <- right_join(training_filtered,new_interest_topics, by = "topic_id")
  
sums <- training_filtered %>%
  group_by(userID,category) %>%
  summarise(lti = sum(ltiFeatures), sti = sum(stiFeatures))

categories <- sort(unique(new_table$a))



sums_lti <- sums[1:3]
sums_sti <- sums[c(1,2,4)]

lti <- cast(sums_lti, userID~category)
sti <- cast(sums_sti, userID~category)

lti[is.na(lti)] <- 0
sti[is.na(sti)] <- 0

inAudience <- training_filtered[1:2]
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

write.csv(lti_2,"lti_training.csv")
write.csv(sti_2,"sti_training.csv")

threshold = .01
x <- lti_2[2:26]
x[x>threshold] <- TRUE
x[x<=threshold] <- FALSE
x <- cbind(sti_2$inAudience,x,sti_2$userID)

y<-split(x, x[,1])
true_counts <- y$`1`
false_counts <- y$`0`

true_sum <- as.data.frame(colSums(true_counts[, 2:25]))
true_sum <- cbind(rownames(true_sum),true_sum)
colnames(true_sum) <- c("Category","Counts")
attach(true_sum)
true_sum <- true_sum[order(-Counts),]

png("Plot1.png", width = 8, height = 4, units = 'in', res = 300)
op <- par(mar=c(11,4,4,2))
barplot(height = true_sum$Counts, names.arg = true_sum$Category,horiz=F,las=2,
        main = "Number of Trues per Category", ylab = "Count")
rm(op)
dev.off()

false_sum <- as.data.frame(colSums(false_counts[, 2:25]))
false_sum <- cbind(rownames(false_sum),false_sum)
colnames(false_sum) <- c("Category","Counts")
attach(false_sum)
false_sum <- false_sum[order(-Counts),]

png("Plot2.png", width = 8, height = 4, units = 'in', res = 300)
op <- par(mar=c(11,4,4,2))
barplot(height = false_sum$Counts, names.arg = false_sum$Category,horiz=F,las=2,
        main = "Number of Falses per Category", ylab = "Count")
rm(op)
dev.off()

true_sum <- as.data.frame(colSums(true_counts[, 2:25]))
false_sum <- as.data.frame(colSums(false_counts[, 2:25]))
percents <- true_sum[1]/(true_sum[1]+false_sum[1])
percents <- cbind(rownames(percents),percents)
colnames(percents) <- c("Category","Percents")
attach(percents)
percents <- percents[order(-Percents),]

png("Plot3.png", width = 8, height = 4, units = 'in', res = 300)
op <- par(mar=c(11,4,4,2))
barplot(height = percents$Percents, names.arg = percents$Category,horiz=F,las=2,
        main="Proportion of Trues")
rm(op)
dev.off()

colnames(true_counts)[c(1,27)] <- c("inAudience","userID")

c <- list()

for (i in 2:26){
a <- true_counts[c(i,27)]
a[a==0] <- NA
b<-a[complete.cases(a),]
c[[i-1]] <- b$userID
}

jaccard <- matrix(0,nrow=25,ncol=25)


for (i in 1:25){
  for (j in i:25){
    if (i != j){
      cat1 <- c[[i]]
      cat2 <- c[[j]]
      intersect <- length(intersect(cat1,cat2))
      union <- length(union(cat1,cat2))
      jaccard[i,j] <- intersect/union
    }
    else{
      jaccard[i,j]<-NA
    }
  }
}

jaccard[lower.tri(jaccard)] <- NA
melted_jaccard <- melt(jaccard)

rownames(jaccard) <- colnames(true_counts)[2:26]
colnames(jaccard) <- colnames(true_counts)[2:26]



ggplot(data = melted_jaccard, aes(x=X2, y=X1, fill=value)) + 
  geom_tile() + theme(axis.text.x = element_text(angle = 90),axis.title.x=element_blank(),axis.title.y=element_blank())+
  labs(title = "Pairwise Jaccard")

ggsave("prop.png", plot = last_plot(), device = NULL, path = NULL,
       scale = 1, width = NA, height = NA, units = c("in", "cm", "mm"),
       dpi = 300, limitsize = TRUE)
# jaccard <- as.data.frame(jaccard)
# colnames(jaccard) <- colnames(true_counts)[2:26]
# rownames(jaccard) <- colnames(true_counts)[2:26]
# 
# categories <- cbind(c(1:25),colnames(jaccard))
# categories <- as.data.frame(categories)
# categories$V1 <- as.numeric(categories$V1)
# a <- right_join(categories,melted_jaccard,by = c("V1"="X1"))
# a <- right_join(categories,a,by = c("V1"="X2"))
# 
# ggplot(data = a, aes(x=V2.y, y=V2.x, fill=value)) + 
#   geom_tile()
