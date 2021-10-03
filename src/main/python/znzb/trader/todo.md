# Notes

Accounts:
  - bank (currency)
  - cash  (currency)

  - asset (currency)
  - liability (currency)

  - income (currency)
  - expense (currency)

  - equity (currency)

## Transaction

### Begin balance

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  1 | bank             | 100.00 |  1 | equity           | 100.00 |
|    | Total            | 100.00 |    | Total            | 100.00 |

### Buy BTC

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  2 | cash = BTC 0.001 |  99.75 |  2 | bank             | 100.00 |
|  2 | expense          |   0.25 |    |                  |        |
|    | Total            | 100.00 |    | Total            | 100.00 |

### Sell BTC

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  3 | bank             | 109.75 |  3 | cash = BTC 0.001 | 110.00 |
|  3 | expense          |   0.25 |    |                  |        |
|    | Total            | 110.00 |    | Total            | 110.00 |

## Balance

### Bank

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  1 | equity           | 100.00 |  2 | cash = BTC 0.001 |  99.75 |
|  3 | cash = BTC 0.001 | 110.00 |  2 | expense          |   0.25 |
|    |                  |        |  3 | expense          |   0.25 |
|    |                  |        |  5 | equity           | 109.75 |
|    | Total            | 210.00 |    | Total            | 210.00 |

### Cash BTC

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  2 | bank = BTC 0.001 |  99.75 |  3 | bank = BTC 0.001 | 110.00 |
|  4 | profit           |  10.25 |    |                  |        |
|    | Total            | 110.00 |    | Total            | 110.00 |

### Expense

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  2 | bank             |   0.25 |  5 | equity           |   0.50 |
|  3 | bank             |   0.25 |    |                  |        |
|    | Total            |   0.50 |    | Total            |   0.50 |

### Profit & Loss

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  5 | equity           |  10.25 |  4 | cash BTC         |  10.25 |
|    | Total            |  10.25 |    | Total            |  10.25 |

### Equity

| No | Debet            |        | No | Credit           |        | 
|----|:---------------- | ------:|----|:---------------- | ------:|
|  5 | bank             | 109.75 |  1 | bank             | 100.00 |
|  5 | expense          |   0.50 |  5 | profit & loss    |  10.25 |
|    | Total            | 110.00 |    | Total            | 110.00 |
