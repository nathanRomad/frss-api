from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class AnalyticsView(ViewSet):

    def list(self, request):
        """Handle GET requests to answers resource
        Returns:
            Response -- JSON serialized list of answers
        """
        user = request.auth.user

        # Budget & Protection
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
        retirementSavings = user.answers_set.get(question__id=25).input_answer

        # Data for bar chart
        data = [
            {
                "country": "AD",
                "hot dog": 4,
                "hot dogColor": "hsl(233, 70%, 50%)",
                "burger": 93,
                "burgerColor": "hsl(270, 70%, 50%)",
                "sandwich": 159,
                "sandwichColor": "hsl(319, 70%, 50%)",
                "kebab": 134,
                "kebabColor": "hsl(172, 70%, 50%)",
                "fries": 137,
                "friesColor": "hsl(160, 70%, 50%)",
                "donut": 165,
                "donutColor": "hsl(105, 70%, 50%)"
            },
            {
                "country": "AE",
                "hot dog": 10,
                "hot dogColor": "hsl(204, 70%, 50%)",
                "burger": 58,
                "burgerColor": "hsl(227, 70%, 50%)",
                "sandwich": 114,
                "sandwichColor": "hsl(159, 70%, 50%)",
                "kebab": 34,
                "kebabColor": "hsl(320, 70%, 50%)",
                "fries": 192,
                "friesColor": "hsl(165, 70%, 50%)",
                "donut": 37,
                "donutColor": "hsl(255, 70%, 50%)"
            },
            {
                "country": "AF",
                "hot dog": 36,
                "hot dogColor": "hsl(64, 70%, 50%)",
                "burger": 62,
                "burgerColor": "hsl(90, 70%, 50%)",
                "sandwich": 49,
                "sandwichColor": "hsl(25, 70%, 50%)",
                "kebab": 131,
                "kebabColor": "hsl(74, 70%, 50%)",
                "fries": 73,
                "friesColor": "hsl(28, 70%, 50%)",
                "donut": 142,
                "donutColor": "hsl(183, 70%, 50%)"
            },
            {
                "country": "AG",
                "hot dog": 37,
                "hot dogColor": "hsl(9, 70%, 50%)",
                "burger": 79,
                "burgerColor": "hsl(199, 70%, 50%)",
                "sandwich": 57,
                "sandwichColor": "hsl(64, 70%, 50%)",
                "kebab": 38,
                "kebabColor": "hsl(68, 70%, 50%)",
                "fries": 22,
                "friesColor": "hsl(43, 70%, 50%)",
                "donut": 118,
                "donutColor": "hsl(197, 70%, 50%)"
            },
            {
                "country": "AI",
                "hot dog": 200,
                "hot dogColor": "hsl(218, 70%, 50%)",
                "burger": 92,
                "burgerColor": "hsl(246, 70%, 50%)",
                "sandwich": 116,
                "sandwichColor": "hsl(175, 70%, 50%)",
                "kebab": 11,
                "kebabColor": "hsl(154, 70%, 50%)",
                "fries": 187,
                "friesColor": "hsl(146, 70%, 50%)",
                "donut": 8,
                "donutColor": "hsl(141, 70%, 50%)"
            },
            {
                "country": "AL",
                "hot dog": 188,
                "hot dogColor": "hsl(259, 70%, 50%)",
                "burger": 81,
                "burgerColor": "hsl(3, 70%, 50%)",
                "sandwich": 52,
                "sandwichColor": "hsl(280, 70%, 50%)",
                "kebab": 92,
                "kebabColor": "hsl(303, 70%, 50%)",
                "fries": 188,
                "friesColor": "hsl(13, 70%, 50%)",
                "donut": 2,
                "donutColor": "hsl(171, 70%, 50%)"
            },
            {
                "country": "AM",
                "hot dog": 160,
                "hot dogColor": "hsl(21, 70%, 50%)",
                "burger": 128,
                "burgerColor": "hsl(86, 70%, 50%)",
                "sandwich": 88,
                "sandwichColor": "hsl(97, 70%, 50%)",
                "kebab": 14,
                "kebabColor": "hsl(330, 70%, 50%)",
                "fries": 154,
                "friesColor": "hsl(48, 70%, 50%)",
                "donut": 168,
                "donutColor": "hsl(129, 70%, 50%)"
            }
        ]

    #     lineData = [
    # {
    #     "id": "japan",
    #     "color": "hsl(314, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 178
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 75
    #     },
    #     {
    #         "x": "boat",
    #         "y": 82
    #     },
    #     {
    #         "x": "train",
    #         "y": 282
    #     },
    #     {
    #         "x": "subway",
    #         "y": 213
    #     },
    #     {
    #         "x": "bus",
    #         "y": 142
    #     },
    #     {
    #         "x": "car",
    #         "y": 190
    #     },
    #     {
    #         "x": "moto",
    #         "y": 183
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 22
    #     },
    #     {
    #         "x": "horse",
    #         "y": 30
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 217
    #     },
    #     {
    #         "x": "others",
    #         "y": 164
    #     }
    #     ]
    # },
    # {
    #     "id": "france",
    #     "color": "hsl(61, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 145
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 253
    #     },
    #     {
    #         "x": "boat",
    #         "y": 97
    #     },
    #     {
    #         "x": "train",
    #         "y": 88
    #     },
    #     {
    #         "x": "subway",
    #         "y": 211
    #     },
    #     {
    #         "x": "bus",
    #         "y": 212
    #     },
    #     {
    #         "x": "car",
    #         "y": 9
    #     },
    #     {
    #         "x": "moto",
    #         "y": 273
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 101
    #     },
    #     {
    #         "x": "horse",
    #         "y": 154
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 248
    #     },
    #     {
    #         "x": "others",
    #         "y": 58
    #     }
    #     ]
    # },
    # {
    #     "id": "us",
    #     "color": "hsl(282, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 25
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 143
    #     },
    #     {
    #         "x": "boat",
    #         "y": 30
    #     },
    #     {
    #         "x": "train",
    #         "y": 282
    #     },
    #     {
    #         "x": "subway",
    #         "y": 89
    #     },
    #     {
    #         "x": "bus",
    #         "y": 17
    #     },
    #     {
    #         "x": "car",
    #         "y": 0
    #     },
    #     {
    #         "x": "moto",
    #         "y": 217
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 243
    #     },
    #     {
    #         "x": "horse",
    #         "y": 123
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 131
    #     },
    #     {
    #         "x": "others",
    #         "y": 100
    #     }
    #     ]
    # },
    # {
    #     "id": "germany",
    #     "color": "hsl(278, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 287
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 176
    #     },
    #     {
    #         "x": "boat",
    #         "y": 73
    #     },
    #     {
    #         "x": "train",
    #         "y": 52
    #     },
    #     {
    #         "x": "subway",
    #         "y": 121
    #     },
    #     {
    #         "x": "bus",
    #         "y": 222
    #     },
    #     {
    #         "x": "car",
    #         "y": 237
    #     },
    #     {
    #         "x": "moto",
    #         "y": 1
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 61
    #     },
    #     {
    #         "x": "horse",
    #         "y": 269
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 15
    #     },
    #     {
    #         "x": "others",
    #         "y": 272
    #     }
    #     ]
    # },
    # {
    #     "id": "norway",
    #     "color": "hsl(50, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 234
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 20
    #     },
    #     {
    #         "x": "boat",
    #         "y": 76
    #     },
    #     {
    #         "x": "train",
    #         "y": 188
    #     },
    #     {
    #         "x": "subway",
    #         "y": 86
    #     },
    #     {
    #         "x": "bus",
    #         "y": 200
    #     },
    #     {
    #         "x": "car",
    #         "y": 34
    #     },
    #     {
    #         "x": "moto",
    #         "y": 234
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 121
    #     },
    #     {
    #         "x": "horse",
    #         "y": 221
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 169
    #     },
    #     {
    #         "x": "others",
    #         "y": 41
    #     }
    #     ]
    # }
    # ]
        # Build out an object to send back to the front with the data calculations provided
        analysis = {
            "detailedAnalysisOne": {
                "totalLiabilities": totalLiabilities,
                "retirementSavings": retirementSavings
            },
            "data": data
        }
        # Send the object to the client
        return Response(analysis)
