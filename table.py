import pandas as pd

data = [
    {
        "": "Cash flow from operating activities",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Loss before tax",
        "Three months ended June 30, 2024": -6110.07,
        "Three months ended June 30, 2023": -5640.84,
        "Year ended March 31, 2024": -23502.43,
        "Year ended March 31, 2023": -41793.05,
        "Year ended March 31, 2022": -36288.96
    },
    {
        "": "Adjustments to reconcile the loss before tax to net cash flows:",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Depreciation and amortisation expense",
        "Three months ended June 30, 2024": 1216.72,
        "Three months ended June 30, 2023": 912.98,
        "Year ended March 31, 2024": 4205.85,
        "Year ended March 31, 2023": 2857.86,
        "Year ended March 31, 2022": 1700.90
    },
    {
        "": "Income on investments carried at fair value through profit or loss",
        "Three months ended June 30, 2024": -514.57,
        "Three months ended June 30, 2023": -758.87,
        "Year ended March 31, 2024": -2401.47,
        "Year ended March 31, 2023": -2114.43,
        "Year ended March 31, 2022": -2547.91
    },
    {
        "": "Interest income on security deposits carried at amortised cost",
        "Three months ended June 30, 2024": -16.29,
        "Three months ended June 30, 2023": -15.79,
        "Year ended March 31, 2024": -64.22,
        "Year ended March 31, 2023": -55.42,
        "Year ended March 31, 2022": -37.78
    },
    {
        "": "Interest expense on financial liabilities carried at amortised cost",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": 35.62,
        "Year ended March 31, 2023": 3.01,
        "Year ended March 31, 2022": ""
    },
    {
        "": "Gain on termination of leases",
        "Three months ended June 30, 2024": -76.23,
        "Three months ended June 30, 2023": -6.33,
        "Year ended March 31, 2024": -73.25,
        "Year ended March 31, 2023": -167.74,
        "Year ended March 31, 2022": -246.34
    },
    {
        "": "Impairment on property, plant and equipment (Refer note 29)",
        "Three months ended June 30, 2024": 47.67,
        "Three months ended June 30, 2023": 6.70,
        "Year ended March 31, 2024": 127.70,
        "Year ended March 31, 2023": 92.56,
        "Year ended March 31, 2022": 105.19
    },
    {
        "": "Impairment on goodwill and other intangible assets (Refer note 29)",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": 178.24,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": 1566.30
    },
    {
        "": "Write-down of inventories to net realisable value (Refer note 29)",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": 60.55
    },
    {
        "": "Share based payment expense",
        "Three months ended June 30, 2024": 2593.14,
        "Three months ended June 30, 2023": 1397.46,
        "Year ended March 31, 2024": 5962.62,
        "Year ended March 31, 2023": 3373.52,
        "Year ended March 31, 2022": 4858.15
    },
    {
        "": "Loss on disposal/write off of property, plant and equipment (net)",
        "Three months ended June 30, 2024": 2.07,
        "Three months ended June 30, 2023": 21.73,
        "Year ended March 31, 2024": 152.45,
        "Year ended March 31, 2023": 28.45,
        "Year ended March 31, 2022": 24.34
    },
    {
        "": "Advances/ deposits/ receivables written off",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": 7.05,
        "Year ended March 31, 2022": 12.63
    },
    {
        "": "Allowances for doubtful debts and receivables",
        "Three months ended June 30, 2024": 104.52,
        "Three months ended June 30, 2023": 73.71,
        "Year ended March 31, 2024": 635.89,
        "Year ended March 31, 2023": 333.96,
        "Year ended March 31, 2022": 104.32
    },
    {
        "": "Allowances for doubtful advances",
        "Three months ended June 30, 2024": 2.68,
        "Three months ended June 30, 2023": 121.52,
        "Year ended March 31, 2024": 172.74,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Expenses incurred towards proposed Initial Public Offering",
        "Three months ended June 30, 2024": 83.03,
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Interest on borrowings",
        "Three months ended June 30, 2024": 40.80,
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": 76.67,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": 24.80
    },
    {
        "": "Interest on lease liabilities",
        "Three months ended June 30, 2024": 148.70,
        "Three months ended June 30, 2023": 165.37,
        "Year ended March 31, 2024": 601.74,
        "Year ended March 31, 2023": 561.88,
        "Year ended March 31, 2022": 443.96
    },
    {
        "": "Interest income",
        "Three months ended June 30, 2024": -237.51,
        "Three months ended June 30, 2023": -333.04,
        "Year ended March 31, 2024": -1145.41,
        "Year ended March 31, 2023": -1213.67,
        "Year ended March 31, 2022": -627.78
    },
    {
        "": "Share of loss of associate",
        "Three months ended June 30, 2024": -0.90,
        "Three months ended June 30, 2023": -5.00,
        "Year ended March 31, 2024": 66.14,
        "Year ended March 31, 2023": 1.03,
        "Year ended March 31, 2022": 10.16
    },
    {
        "": "Provision/ liability no longer required written back",
        "Three months ended June 30, 2024": -32.54,
        "Three months ended June 30, 2023": -82.57,
        "Year ended March 31, 2024": -118.85,
        "Year ended March 31, 2023": -311.70,
        "Year ended March 31, 2022": -27.29
    },
    {
        "": "Interest on income tax refund",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": -63.51,
        "Year ended March 31, 2023": -80.67,
        "Year ended March 31, 2022": -18.22
    },
    {
        "": "Profit on sale of investment in associate",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": -654.60
    },
    {
        "": "Profit on sale of business undertaking",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": -533.67,
        "Year ended March 31, 2022": ""
    },
    {
        "": "Operating cash flow before working capital adjustments",
        "Three months ended June 30, 2024": -2748.78,
        "Three months ended June 30, 2023": -4142.97,
        "Year ended March 31, 2024": -15153.48,
        "Year ended March 31, 2023": -39011.03,
        "Year ended March 31, 2022": -31537.58
    },
    {
        "": "Movements in working capital :",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "(Increase) / decrease in inventories",
        "Three months ended June 30, 2024": -76.08,
        "Three months ended June 30, 2023": -2.62,
        "Year ended March 31, 2024": -126.19,
        "Year ended March 31, 2023": 71.08,
        "Year ended March 31, 2022": -77.03
    },
    {
        "": "(Increase) / decrease in trade receivables",
        "Three months ended June 30, 2024": -2361.92,
        "Three months ended June 30, 2023": 1048.12,
        "Year ended March 31, 2024": 565.00,
        "Year ended March 31, 2023": 410.60,
        "Year ended March 31, 2022": -9566.90
    },
    {
        "": "(Increase) in other financial assets",
        "Three months ended June 30, 2024": -541.34,
        "Three months ended June 30, 2023": -2008.42,
        "Year ended March 31, 2024": -2062.64,
        "Year ended March 31, 2023": -3112.31,
        "Year ended March 31, 2022": -2158.69
    },
    {
        "": "(Increase) / decrease in other assets",
        "Three months ended June 30, 2024": -397.60,
        "Three months ended June 30, 2023": 387.48,
        "Year ended March 31, 2024": 1026.40,
        "Year ended March 31, 2023": 1285.91,
        "Year ended March 31, 2022": -3342.66
    },
    {
        "": "Increase / (decrease) in trade payable",
        "Three months ended June 30, 2024": 1118.24,
        "Three months ended June 30, 2023": 150.28,
        "Year ended March 31, 2024": 67.68,
        "Year ended March 31, 2023": -662.76,
        "Year ended March 31, 2022": 6078.19
    },
    {
        "": "Increase / (decrease) in financial liabilities",
        "Three months ended June 30, 2024": -64.70,
        "Three months ended June 30, 2023": 3412.61,
        "Year ended March 31, 2024": 2238.69,
        "Year ended March 31, 2023": 516.42,
        "Year ended March 31, 2022": 1205.51
    },
    {
        "": "Increase / (decrease) in other liabilities",
        "Three months ended June 30, 2024": 37.33,
        "Three months ended June 30, 2023": -334.25,
        "Year ended March 31, 2024": 184.56,
        "Year ended March 31, 2023": 45.48,
        "Year ended March 31, 2022": 570.55
    },
    {
        "": "Increase / (decrease) in contract liabilities",
        "Three months ended June 30, 2024": -49.96,
        "Three months ended June 30, 2023": -66.36,
        "Year ended March 31, 2024": 149.06,
        "Year ended March 31, 2023": 39.34,
        "Year ended March 31, 2022": 178.30
    },
    {
        "": "Increase / (decrease) in provisions",
        "Three months ended June 30, 2024": 56.22,
        "Three months ended June 30, 2023": 18.12,
        "Year ended March 31, 2024": -54.43,
        "Year ended March 31, 2023": 267.51,
        "Year ended March 31, 2022": 236.80
    },
    {
        "": "Cash used in operating activities",
        "Three months ended June 30, 2024": -5028.59,
        "Three months ended June 30, 2023": -1538.01,
        "Year ended March 31, 2024": -13165.35,
        "Year ended March 31, 2023": -40149.76,
        "Year ended March 31, 2022": -38413.51
    },
    {
        "": "Income tax paid (net of refund)",
        "Three months ended June 30, 2024": -137.68,
        "Three months ended June 30, 2023": -199.81,
        "Year ended March 31, 2024": 38.00,
        "Year ended March 31, 2023": -449.33,
        "Year ended March 31, 2022": -590.36
    },
    {
        "": "Net cash used in operating activities (A)",
        "Three months ended June 30, 2024": -5166.27,
        "Three months ended June 30, 2023": -1737.82,
        "Year ended March 31, 2024": -13127.35,
        "Year ended March 31, 2023": -40599.09,
        "Year ended March 31, 2022": -39003.87
    },
    {
        "": "Cash flow from investing activities",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Purchase of investments",
        "Three months ended June 30, 2024": -22302.69,
        "Three months ended June 30, 2023": -15367.08,
        "Year ended March 31, 2024": -82721.27,
        "Year ended March 31, 2023": -97678.69,
        "Year ended March 31, 2022": -210735.66
    },
    {
        "": "Proceeds from sale/ maturity of investments",
        "Three months ended June 30, 2024": 27781.47,
        "Three months ended June 30, 2023": 21723.52,
        "Year ended March 31, 2024": 100122.19,
        "Year ended March 31, 2023": 138437.43,
        "Year ended March 31, 2022": 118881.46
    },
    {
        "": "Purchase of property, plant and equipment and other intangible assets",
        "Three months ended June 30, 2024": -699.21,
        "Three months ended June 30, 2023": -862.95,
        "Year ended March 31, 2024": -3517.14,
        "Year ended March 31, 2023": -1682.99,
        "Year ended March 31, 2022": -2913.48
    },
    {
        "": "Proceeds from disposal of property, plant and equipment and other intangible assets",
        "Three months ended June 30, 2024": 9.25,
        "Three months ended June 30, 2023": 39.01,
        "Year ended March 31, 2024": 77.02,
        "Year ended March 31, 2023": 110.13,
        "Year ended March 31, 2022": 639.19
    },
    {
        "": "Investment in bank deposits, net",
        "Three months ended June 30, 2024": -204.91,
        "Three months ended June 30, 2023": 299.89,
        "Year ended March 31, 2024": 275.97,
        "Year ended March 31, 2023": -235.33,
        "Year ended March 31, 2022": 1722.56
    },
    {
        "": "Interest received",
        "Three months ended June 30, 2024": 375.09,
        "Three months ended June 30, 2023": 308.75,
        "Year ended March 31, 2024": 761.85,
        "Year ended March 31, 2023": 727.92,
        "Year ended March 31, 2022": 204.74
    },
    {
        "": "Payments towards purchase of undertaking on slump sale",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": -220.74
    },
    {
        "": "Investment in an associate company",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": -16.32
    },
    {
        "": "Proceeds from sale of an associate company",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": 836.85
    },
    {
        "": "Acquisition of subsidiary (consideration paid in cash)",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": -18.42,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Inter-corporate loan given",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": -395.62,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Net cash flow from/ (used in) investing activities (B)",
        "Three months ended June 30, 2024": 4959.00,
        "Three months ended June 30, 2023": 6141.14,
        "Year ended March 31, 2024": 14584.58,
        "Year ended March 31, 2023": 39678.47,
        "Year ended March 31, 2022": -91601.40
    },
    {
        "": "Cash flow from financing activities",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Proceeds from issue of equity shares",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": 2.62
    },
    {
        "": "Proceeds from issue of instruments entirely equity in nature",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": 139055.63
    },
    {
        "": "Payment of principal portion of lease liabilities",
        "Three months ended June 30, 2024": -480.03,
        "Three months ended June 30, 2023": -360.57,
        "Year ended March 31, 2024": -1636.46,
        "Year ended March 31, 2023": -1450.49,
        "Year ended March 31, 2022": -617.14
    },
    {
        "": "Payment of interest portion of lease liabilities",
        "Three months ended June 30, 2024": -148.70,
        "Three months ended June 30, 2023": -165.37,
        "Year ended March 31, 2024": -601.74,
        "Year ended March 31, 2023": -264.99,
        "Year ended March 31, 2022": -443.96
    },
    {
        "": "Share issue expenses",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": -709.05
    },
    {
        "": "Transaction costs related to proposed Initial Public Offering",
        "Three months ended June 30, 2024": -83.03,
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": "",
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Proceeds from borrowings",
        "Three months ended June 30, 2024": 1249.89,
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": 3976.97,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Repayment of borrowings",
        "Three months ended June 30, 2024": -596.35,
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": -2900.82,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": -918.02
    },
    {
        "": "Interest paid",
        "Three months ended June 30, 2024": -60.68,
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": -65.90,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": -28.60
    },
    {
        "": "Net cash flow from/ (used in) financing activities (C)",
        "Three months ended June 30, 2024": -118.90,
        "Three months ended June 30, 2023": -525.94,
        "Year ended March 31, 2024": -1227.95,
        "Year ended March 31, 2023": -1715.48,
        "Year ended March 31, 2022": 136341.48
    },
    {
        "": "Net increase in cash and cash equivalents (A+B+C)",
        "Three months ended June 30, 2024": -326.17,
        "Three months ended June 30, 2023": 3877.38,
        "Year ended March 31, 2024": 229.28,
        "Year ended March 31, 2023": -2636.10,
        "Year ended March 31, 2022": 5736.21
    },
    {
        "": "Cash and cash equivalents acquired through business combination",
        "Three months ended June 30, 2024": "",
        "Three months ended June 30, 2023": "",
        "Year ended March 31, 2024": 136.60,
        "Year ended March 31, 2023": "",
        "Year ended March 31, 2022": ""
    },
    {
        "": "Cash and cash equivalents at the beginning of the period/ year",
        "Three months ended June 30, 2024": 8691.09,
        "Three months ended June 30, 2023": 8325.21,
        "Year ended March 31, 2024": 8325.21,
        "Year ended March 31, 2023": 10961.31,
        "Year ended March 31, 2022": 5225.10
    },
    {
        "": "Cash and cash equivalents at the end of the period/ year (Refer note 2.25 and note below)",
        "Three months ended June 30, 2024": 8364.92,
        "Three months ended June 30, 2023": 12202.59,
        "Year ended March 31, 2024": 8691.09,
        "Year ended March 31, 2023": 8325.21,
        "Year ended March 31, 2022": 10961.31
    }
]

df = pd.DataFrame(data)
