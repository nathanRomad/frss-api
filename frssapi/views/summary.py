from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class SummaryView(ViewSet):

    def list(self, request):
        """Handle GET requests to answers resource 
        Returns:
            Response -- JSON serialized list of answers
        """
        user = request.auth.user

        ### Budget & Protection
        # Subtract Users totalAssets from totalLiabilities
        liabilities = user.answers_set.filter(question__id__in=[7, 8])
        totalLiabilities = liabilities[1].input_answer - \
            liabilities[0].input_answer

        # Add Users total income with any additional income to provide a totalAssets
        assets = user.answers_set.filter(question__id__in=[4, 5])
        totalAnnualIncome = assets[1].input_answer+assets[0].input_answer

        # Users monthly income
        income = user.answers_set.filter(question__id__in=[4])
        monthlyIncome = round(income[0].input_answer/12, 2)

        # Living Expenses
        monthlyLivingExpenses = user.answers_set.filter(question__id__in=[9])
        incomeAfterLivingExpenses = monthlyIncome - \
            monthlyLivingExpenses[0].input_answer
        ratioOfLivingExpenses = round(
            monthlyLivingExpenses[0].input_answer/monthlyIncome, 2)

        ###Security & Legal
        # Insurance
        rentersInsurance = user.answers_set.get(question__id=12).option.text
        vehicleInsurance = user.answers_set.get(question__id=14).option.text
        healthInsurance = user.answers_set.get(question__id=15).option.text
        lifeInsurance = user.answers_set.get(question__id=16).option.text
        disabilityInsurance = user.answers_set.get(question__id=17).option.text
        longTermCarePlan = user.answers_set.get(question__id=18).option.text
        # # Legal Documents
        will = user.answers_set.get(question__id=19).option.text
        healthCareDirective = user.answers_set.get(question__id=20).option.text
        powerOfAttorney = user.answers_set.get(question__id=21).option.text

        # Retirement
        # Retirement Savings
        retirementSavings = user.answers_set.get(question__id=25).input_answer
        # RetirementContributions
        monthlyRetirementContributions = user.answers_set.get(question__id=24).input_answer

        # Financial Readiness Score
        # Option Answer Scoring
        optionScore = 0
        optionAnswers = user.answers_set.filter(option__isnull=False)
        for answer in optionAnswers:
            optionScore += answer.option.point_value
        inputAnswers = user.answers_set.filter(input_answer__isnull=False)
        # Input Answer Scoring
        allInputAnswers = 0
        for answer in inputAnswers:
            allInputAnswers += answer.input_answer
        averageInputAnswer = round(allInputAnswers/len(inputAnswers))
        inputScore = round(averageInputAnswer/1000)
        # Combined Score
        initialScore = inputScore + optionScore / 29
        financialReadinessScore = round(initialScore*4)

        # Build out an object to send back to the front with the data calculations provided
        analysis = {
            "budgetAndProtection": {
                "totalLiabilities": totalLiabilities,
                "totalAnnualIncome": totalAnnualIncome,
                "monthlyIncome": monthlyIncome,
                "ratioOfLivingExpenses": ratioOfLivingExpenses,
            },
            "securityAndLegal": {
                "rentersInsurance": rentersInsurance,
                "vehicleInsurance": vehicleInsurance,
                "healthInsurance": healthInsurance,
                "lifeInsurance": lifeInsurance,
                "disabilityInsurance": disabilityInsurance,
                "longTermCarePlan": longTermCarePlan,
                "will": will,
                "healthCareDirective": healthCareDirective,
                "powerOfAttorney": powerOfAttorney
            },
            "retirement": {
                "retirementSavings": retirementSavings,
                "monthlyRetirementContributions": monthlyRetirementContributions
            },
            "score": {
                "averageInputAnswer": averageInputAnswer,
                "optionScore": optionScore,
                "inputScore": inputScore,
                "financialReadinessScore": financialReadinessScore
            }
        }
        # Send the object to the client
        return Response(analysis)
