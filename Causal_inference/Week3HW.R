# install and load packages
p_needed <- c("tableone", "Matching", "MatchIt")

packages <- rownames(installed.packages())
p_to_install <- p_needed[!(p_needed %in% packages)]

if (length(p_to_install) > 0) {
  install.packages(p_to_install)
}

output = lapply(p_needed, require, character.only = TRUE)

#  load the lalonde data (which is in the MatchIt package
data(lalonde)

# The data have n=614 subjects and 10 variables
# age age in years. 
# educ years of schooling. 
# black indicator variable for blacks. 
# hispan indicator variable for Hispanics. 
# married indicator variable for marital status. 
# nodegree indicator variable for high school diploma. 
# re74 real earnings in 1974. 
# re75 real earnings in 1975. 
# re78 real earnings in 1978. 
# treat an indicator variable for treatment status.

# outcome 
# re78 – post-intervention income
# treatment
# treat – which is equal to 1 if the subject received the labor training and equal
# to 0 otherwise.

# potential confounding
# variables are: age, educ, black, hispan, married, nodegree, re74, re75.
library(dplyr)
lalonde <- lalonde %>% mutate(black = as.numeric(race == "black"),
                   hispan = as.numeric(race == "hispan")
                   )
xvars <- c("age", "educ", "black", "hispan", "married", 
           "nodegree", "re74", "re75")
table1<- CreateTableOne(vars=xvars,strata="treat", data=lalonde, test=FALSE)
## include standardized mean difference (SMD)
print(table1,smd=TRUE)

##########################
#propensity score matching
#########################

#fit a propensity score model. logistic regression

psmodel<-glm(treat ~ age + educ + black +hispan +
               married + nodegree + re74 + re75,
             family=binomial(),data=lalonde)

#show coefficients etc
summary(psmodel)
#create propensity score
pscore<-psmodel$fitted.values
max(pscore)
set.seed(931139)
logit <- function(p) {log(p)-log(1-p)}

psmatch <- Match(Tr = lalonde$treat, M = 1,
                 X= pscore, 
                 replace = FALSE,
                 caliper = 0.1)

xvars <- c("age", "educ", "black", "hispan", "married", 
           "nodegree", "re74", "re75")
matched<-lalonde[unlist(psmatch[c("index.treated","index.control")]), ]
#get standardized differences
matchedtab1<-CreateTableOne(vars=xvars, strata ="treat", 
                            data=matched, test = FALSE)
print(matchedtab1, smd = TRUE)

matched %>% group_by(treat) %>% summarise(mean(re78))

#outcome analysis
y_trt<-matched$re78[matched$treat==1]
y_con<-matched$re78[matched$treat==0]

#pairwise difference
diffy<-y_trt-y_con

#paired t-test
t.test(diffy)


