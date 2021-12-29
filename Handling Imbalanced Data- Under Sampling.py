{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import sklearn\n",
    "import scipy\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from sklearn.metrics import classification_report,accuracy_score\n",
    "from sklearn.ensemble import IsolationForest\n",
    "from sklearn.neighbors import LocalOutlierFactor\n",
    "from sklearn.svm import OneClassSVM\n",
    "from pylab import rcParams\n",
    "rcParams['figure.figsize'] = 14, 8\n",
    "RANDOM_SEED = 42\n",
    "LABELS = [\"Normal\", \"Fraud\"]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Time</th>\n",
       "      <th>V1</th>\n",
       "      <th>V2</th>\n",
       "      <th>V3</th>\n",
       "      <th>V4</th>\n",
       "      <th>V5</th>\n",
       "      <th>V6</th>\n",
       "      <th>V7</th>\n",
       "      <th>V8</th>\n",
       "      <th>V9</th>\n",
       "      <th>...</th>\n",
       "      <th>V21</th>\n",
       "      <th>V22</th>\n",
       "      <th>V23</th>\n",
       "      <th>V24</th>\n",
       "      <th>V25</th>\n",
       "      <th>V26</th>\n",
       "      <th>V27</th>\n",
       "      <th>V28</th>\n",
       "      <th>Amount</th>\n",
       "      <th>Class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0.0</td>\n",
       "      <td>-1.359807</td>\n",
       "      <td>-0.072781</td>\n",
       "      <td>2.536347</td>\n",
       "      <td>1.378155</td>\n",
       "      <td>-0.338321</td>\n",
       "      <td>0.462388</td>\n",
       "      <td>0.239599</td>\n",
       "      <td>0.098698</td>\n",
       "      <td>0.363787</td>\n",
       "      <td>...</td>\n",
       "      <td>-0.018307</td>\n",
       "      <td>0.277838</td>\n",
       "      <td>-0.110474</td>\n",
       "      <td>0.066928</td>\n",
       "      <td>0.128539</td>\n",
       "      <td>-0.189115</td>\n",
       "      <td>0.133558</td>\n",
       "      <td>-0.021053</td>\n",
       "      <td>149.62</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>0.0</td>\n",
       "      <td>1.191857</td>\n",
       "      <td>0.266151</td>\n",
       "      <td>0.166480</td>\n",
       "      <td>0.448154</td>\n",
       "      <td>0.060018</td>\n",
       "      <td>-0.082361</td>\n",
       "      <td>-0.078803</td>\n",
       "      <td>0.085102</td>\n",
       "      <td>-0.255425</td>\n",
       "      <td>...</td>\n",
       "      <td>-0.225775</td>\n",
       "      <td>-0.638672</td>\n",
       "      <td>0.101288</td>\n",
       "      <td>-0.339846</td>\n",
       "      <td>0.167170</td>\n",
       "      <td>0.125895</td>\n",
       "      <td>-0.008983</td>\n",
       "      <td>0.014724</td>\n",
       "      <td>2.69</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>1.0</td>\n",
       "      <td>-1.358354</td>\n",
       "      <td>-1.340163</td>\n",
       "      <td>1.773209</td>\n",
       "      <td>0.379780</td>\n",
       "      <td>-0.503198</td>\n",
       "      <td>1.800499</td>\n",
       "      <td>0.791461</td>\n",
       "      <td>0.247676</td>\n",
       "      <td>-1.514654</td>\n",
       "      <td>...</td>\n",
       "      <td>0.247998</td>\n",
       "      <td>0.771679</td>\n",
       "      <td>0.909412</td>\n",
       "      <td>-0.689281</td>\n",
       "      <td>-0.327642</td>\n",
       "      <td>-0.139097</td>\n",
       "      <td>-0.055353</td>\n",
       "      <td>-0.059752</td>\n",
       "      <td>378.66</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>1.0</td>\n",
       "      <td>-0.966272</td>\n",
       "      <td>-0.185226</td>\n",
       "      <td>1.792993</td>\n",
       "      <td>-0.863291</td>\n",
       "      <td>-0.010309</td>\n",
       "      <td>1.247203</td>\n",
       "      <td>0.237609</td>\n",
       "      <td>0.377436</td>\n",
       "      <td>-1.387024</td>\n",
       "      <td>...</td>\n",
       "      <td>-0.108300</td>\n",
       "      <td>0.005274</td>\n",
       "      <td>-0.190321</td>\n",
       "      <td>-1.175575</td>\n",
       "      <td>0.647376</td>\n",
       "      <td>-0.221929</td>\n",
       "      <td>0.062723</td>\n",
       "      <td>0.061458</td>\n",
       "      <td>123.50</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2.0</td>\n",
       "      <td>-1.158233</td>\n",
       "      <td>0.877737</td>\n",
       "      <td>1.548718</td>\n",
       "      <td>0.403034</td>\n",
       "      <td>-0.407193</td>\n",
       "      <td>0.095921</td>\n",
       "      <td>0.592941</td>\n",
       "      <td>-0.270533</td>\n",
       "      <td>0.817739</td>\n",
       "      <td>...</td>\n",
       "      <td>-0.009431</td>\n",
       "      <td>0.798278</td>\n",
       "      <td>-0.137458</td>\n",
       "      <td>0.141267</td>\n",
       "      <td>-0.206010</td>\n",
       "      <td>0.502292</td>\n",
       "      <td>0.219422</td>\n",
       "      <td>0.215153</td>\n",
       "      <td>69.99</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>5 rows × 31 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "   Time        V1        V2        V3        V4        V5        V6        V7  \\\n",
       "0   0.0 -1.359807 -0.072781  2.536347  1.378155 -0.338321  0.462388  0.239599   \n",
       "1   0.0  1.191857  0.266151  0.166480  0.448154  0.060018 -0.082361 -0.078803   \n",
       "2   1.0 -1.358354 -1.340163  1.773209  0.379780 -0.503198  1.800499  0.791461   \n",
       "3   1.0 -0.966272 -0.185226  1.792993 -0.863291 -0.010309  1.247203  0.237609   \n",
       "4   2.0 -1.158233  0.877737  1.548718  0.403034 -0.407193  0.095921  0.592941   \n",
       "\n",
       "         V8        V9  ...         V21       V22       V23       V24  \\\n",
       "0  0.098698  0.363787  ...   -0.018307  0.277838 -0.110474  0.066928   \n",
       "1  0.085102 -0.255425  ...   -0.225775 -0.638672  0.101288 -0.339846   \n",
       "2  0.247676 -1.514654  ...    0.247998  0.771679  0.909412 -0.689281   \n",
       "3  0.377436 -1.387024  ...   -0.108300  0.005274 -0.190321 -1.175575   \n",
       "4 -0.270533  0.817739  ...   -0.009431  0.798278 -0.137458  0.141267   \n",
       "\n",
       "        V25       V26       V27       V28  Amount  Class  \n",
       "0  0.128539 -0.189115  0.133558 -0.021053  149.62      0  \n",
       "1  0.167170  0.125895 -0.008983  0.014724    2.69      0  \n",
       "2 -0.327642 -0.139097 -0.055353 -0.059752  378.66      0  \n",
       "3  0.647376 -0.221929  0.062723  0.061458  123.50      0  \n",
       "4 -0.206010  0.502292  0.219422  0.215153   69.99      0  \n",
       "\n",
       "[5 rows x 31 columns]"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data = pd.read_csv('creditcard.csv',sep=',')\n",
    "data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 284807 entries, 0 to 284806\n",
      "Data columns (total 31 columns):\n",
      "Time      284807 non-null float64\n",
      "V1        284807 non-null float64\n",
      "V2        284807 non-null float64\n",
      "V3        284807 non-null float64\n",
      "V4        284807 non-null float64\n",
      "V5        284807 non-null float64\n",
      "V6        284807 non-null float64\n",
      "V7        284807 non-null float64\n",
      "V8        284807 non-null float64\n",
      "V9        284807 non-null float64\n",
      "V10       284807 non-null float64\n",
      "V11       284807 non-null float64\n",
      "V12       284807 non-null float64\n",
      "V13       284807 non-null float64\n",
      "V14       284807 non-null float64\n",
      "V15       284807 non-null float64\n",
      "V16       284807 non-null float64\n",
      "V17       284807 non-null float64\n",
      "V18       284807 non-null float64\n",
      "V19       284807 non-null float64\n",
      "V20       284807 non-null float64\n",
      "V21       284807 non-null float64\n",
      "V22       284807 non-null float64\n",
      "V23       284807 non-null float64\n",
      "V24       284807 non-null float64\n",
      "V25       284807 non-null float64\n",
      "V26       284807 non-null float64\n",
      "V27       284807 non-null float64\n",
      "V28       284807 non-null float64\n",
      "Amount    284807 non-null float64\n",
      "Class     284807 non-null int64\n",
      "dtypes: float64(30), int64(1)\n",
      "memory usage: 67.4 MB\n"
     ]
    }
   ],
   "source": [
    "data.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(284807, 30)\n",
      "(284807,)\n"
     ]
    }
   ],
   "source": [
    "#Create independent and Dependent Features\n",
    "columns = data.columns.tolist()\n",
    "# Filter the columns to remove data we do not want \n",
    "columns = [c for c in columns if c not in [\"Class\"]]\n",
    "# Store the variable we are predicting \n",
    "target = \"Class\"\n",
    "# Define a random state \n",
    "state = np.random.RandomState(42)\n",
    "X = data[columns]\n",
    "Y = data[target]\n",
    "X_outliers = state.uniform(low=0, high=1, size=(X.shape[0], X.shape[1]))\n",
    "# Print the shapes of X & Y\n",
    "print(X.shape)\n",
    "print(Y.shape)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Exploratory Data Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "False"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data.isnull().values.any()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0, 0.5, 'Frequency')"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA1kAAAHwCAYAAABUjaU8AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDMuMC4yLCBodHRwOi8vbWF0cGxvdGxpYi5vcmcvOIA7rQAAIABJREFUeJzt3Xu4ZVV5J+rfJ3jBG6CgIhdBxW7RJIio2HYn3qJgWpG0tqhHiYcETxofozE5IbYJxEsunVZzaI0JRsLF+yVGoxiCxuixY5TScASCNhUkUEIDCgLeAb/zx5o7LopdVRscq4q9632fZz17zm+OOeZYa6N7/2rMOXZ1dwAAABjjDtt6AAAAAGuJkAUAADCQkAUAADCQkAUAADCQkAUAADCQkAUAADCQkAXANldVj6+q87fRtT9TVb+wLa69nKraoaq+VVX7DOrvt6rqT6btB1fVsL/dUlUPrKpvjeoPYK0QsgBWmekX8KXXD6vqu3P7z9/W49uSqtqxqrqq9l2qdfffdffDFnS9O1fVq6tqfVV9u6ourqo/GxVibuVYnjx9z5a+Xxuq6j1V9cilNt19U3ffvbsvWUFfF2/pmt39mu7+vwYMP9N4Hz/X90XdffcRfQOsJUIWwCoz/QJ+9+mX20uSPH2u9o6N21fVjlt/lLcPVVVJ/iLJYUmek2TnJAcm+VKSJ26jYV0yfe/ukeSxSdYn+Z/z4WWU7fl7D7AtCVkAa0xVvXaaHXlXVV2f5P+oqsdW1T9U1Ter6vKqOrGq7ji1X5pZevE023NNVZ04199DqurTVXVtVX29qt45d+xN0+zGdVV1dlX9u7ljO063qv3zdHxdVd0/yaenJudPszn/aeNZmap6WFV9ahrvuVX1c3PH3j6N/2NVdX1Vfbaq9tvEx/HUJE9I8szu/kJ339jd3+zuE7v7lGU+u/2r6pNV9Y3pvZ5eVTvPHX9lVV02vZ8vLwWjqjqkqr441a+oqj/c0vepZy7t7v+a5JQkv7/R92Pfaf8/VtUF03vdUFUvn8b0V0n2mZsVu88mvvevraqbvdeq+qXpfVxWVS/f6LM9YW7/X78vVfWuJPdP8rHper9aG91+WFV7VdVHqurqqrqwqv7PuWOvncb19um9nFdVB23pcwJYjYQsgLXpiCTvzGzm5j1JbkzyK0l2S/K4JIcmefFG5zwtySOTPCKzX86fPNVfl+SjSXZNsleSN8+d87kkP5nkXknen+R9VXXn6divJ3nWdK1dkvxiku8l+enp+MOm2bcPzA+iqu6U5CPTNXdP8vIk76mqB881e16S35que0mS12zic3hyks9299c2cXxjleS1SfZIckCSB07XSVU9LLPP7KDuvmdms2NLt/T9jyR/ONUfPH0Wt8ZfJHlUVd1lmWN/nuTo7r5HZp/1p7r72iRPzzQrNr2unNpv/L1fzk9P4zwsyatWMovW3c9NclmSw6brvWGZZu9J8tXMwthzkvy3qvqZuePPTHJ6Zv89fCzJibfoAWANELIA1qbPdPdfdfcPu/u73X12d39umsm5KMlJSX5mo3N+r7uv7e6Lk/xdZrfVJckNSfZNskd3f6+7/+fSCd19endf3d03JvlvSZZCRjILVa/s7guncZzT3VevYOyPS3KnzELLDd398cx+IT9yrs37u3tdd9+Q5B1zY93YvZNcvoJrLr2f/9Xdn+juH0yh5Y350ed0Y5K7JHlYVe3Y3V+dPstk9hntX1X37u7ru/tzK73m5LLMfibvvMyxG5IcUFX3mD7rL26hr5t97zfR5ne6+zvd/f8lOTXJc2/leG9hmk18dJLjpv9OvphZQHzBXLNPdfeZ3X1TZmFrU983gFVNyAJYmy6d36mqf1tVH62q/11V1yV5dWazWvP+99z2d5IsLWjwiiR3TLJuunXvqLl+/+/ptrlrk1yT5G5z/e6d5J9vw9jvn9kMzfwqeP+SZM8VjHVj38hsVmpFqup+VfXeqvra9Dmdkun9dPdXMvssXp3kyunWt/tNp74os5mvr1TV56vqaSu95mTPJD9Mcu0yx45I8owkl1TV31XVY7bQ16VbOL5xm3/J7DP/cd0/yde7+9sb9b2579vdBlwX4HZHyAJYmzZepvtPk5yX5MHTLW2/ndmtcVvuqPvy7v7F7t4jybFJTqqq/arqCUl+Ncl/yuz2r12TfGuu30uTPGgFY9vYZUn2rqr58e2TZKW3/M37eJLHTs+CrcQfJPl+kp+YPqdfyNzn1N1v7+7HJdkvyQ5Jfm+qf6W7j0xynySvT/KBTdz6tylHJDm7u7+38YFpBvIZU98fSfLupUOb6GslS7TvPbe9T2afeZJ8O8ld547dLze3ub4vS7JbVc0Hp9v6fQNY1YQsgO3DPTKbJfl2VT00t3wea5Oq6j9X1dJsxDcz+0X7pqnPG5N8PbOZrhNy85mJP0vy2qp6UM0cWFX3mm4V+0Zmzzst5++nfl9RVXesqidm9rzYe1c65jlnJvlkkg9W1SNq9jeo7llV/2V+Rm7OPTILGtdW1d5Jfm3uc3hoVT1heubsu9PrpunYC6pqt+5emo3qzGamNmn6TPaqqt/JLMy9cpk2O1XV86rqntOtkdcvXTPJFZmFmnvcis9jyW9Nff9EkqPyo2e3zknyc1W1a1XtkeSlG513RTbxfevuryZZl+R3a7Zs/oGZzfDdYsVLgLVOyALYPrwis1+mr89sVmtTCyIs5zFJzq6qb2e2QMOx099wOiOzmaILk1yc5Lrc/PmnP0zyl0k+MR07KbNnmpLk+CTvrNnqgT8/f7Hu/n5mizocnlmAOzHJ87r7f92KMS/11Ul+PsnfZLYYxXVJzs3sWaC/XeaU4zN7rujaJB9OMr8ox50ze+7s65nd9rZrkldNx56W5IJpRb//nuQ53f2DTQxrn5r9Ad9vZbZwyAFJfrq7lxtPMvu+/ct0++LRmZ5x6u7zpvFdPH2O99nMR7GxzyS5KLPP5ffmrn1Kkgsyu83vr/OjWbMlv5vkd6brvWyZfp+TZP/MPp/3Z/ZM3idvxbgA1oS6+S3vAAAA/DjMZAEAAAwkZAEAAAwkZAEAAAwkZAEAAAwkZAEAAAy047YewO3Fbrvt1vvuu++2HgYAAHA79YUvfOHr3b37ltoJWZN9990369at29bDAAAAbqeq6l9W0s7tggAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAMJWQAAAAPtuK0HAPP2Pe6j23oIcLtw8e//3LYeAgBwG5nJAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGEjIAgAAGGhhIauq9q6qT1bVBVV1flX9ylQ/oaq+VlXnTK+nzZ3zm1W1vqq+UlVPnasfOtXWV9Vxc/X9qupzVXVhVb2nqu401e887a+fju+7qPcJAAAwb5EzWTcmeUV3PzTJIUmOraoDpmNv7O4Dp9cZSTIdOzLJw5IcmuSPq2qHqtohyZuTHJbkgCTPnevnD6a+9k9yTZKjp/rRSa7p7gcneePUDgAAYOEWFrK6+/Lu/uK0fX2SC5LsuZlTDk/y7u7+fnd/Ncn6JI+eXuu7+6Lu/kGSdyc5vKoqyROTvH86/9Qkz5zr69Rp+/1JnjS1BwAAWKit8kzWdLveI5J8biq9pKq+VFUnV9WuU23PJJfOnbZhqm2qfu8k3+zuGzeq36yv6fi1U3sAAICFWnjIqqq7J/lAkpd193VJ3pLkQUkOTHJ5ktcvNV3m9L4N9c31tfHYjqmqdVW17qqrrtrs+wAAAFiJhYasqrpjZgHrHd39F0nS3Vd0903d/cMkb83sdsBkNhO199zpeyW5bDP1ryfZpap23Kh+s76m4zsnuXrj8XX3Sd19cHcfvPvuu/+4bxcAAGChqwtWkrcluaC73zBX32Ou2RFJzpu2P5zkyGllwP2S7J/k80nOTrL/tJLgnTJbHOPD3d1JPpnkWdP5RyX50FxfR03bz0ryt1N7AACAhdpxy01us8cleUGSc6vqnKn2ysxWBzwws9v3Lk7y4iTp7vOr6r1J/imzlQmP7e6bkqSqXpLkzCQ7JDm5u8+f+vuNJO+uqtcm+cfMQl2mr6dX1frMZrCOXOD7BAAA+FcLC1nd/Zks/2zUGZs553VJXrdM/Yzlzuvui/Kj2w3n699L8uxbM14AAIARtsrqggAAANsLIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGCghYWsqtq7qj5ZVRdU1flV9StT/V5VdVZVXTh93XWqV1WdWFXrq+pLVXXQXF9HTe0vrKqj5uqPrKpzp3NOrKra3DUAAAAWbZEzWTcmeUV3PzTJIUmOraoDkhyX5BPdvX+ST0z7SXJYkv2n1zFJ3pLMAlOS45M8Jsmjkxw/F5reMrVdOu/Qqb6pawAAACzUwkJWd1/e3V+ctq9PckGSPZMcnuTUqdmpSZ45bR+e5LSe+Ycku1TVHkmemuSs7r66u69JclaSQ6dj9+zuz3Z3Jzlto76WuwYAAMBCbZVnsqpq3ySPSPK5JPft7suTWRBLcp+p2Z5JLp07bcNU21x9wzL1bOYaG4/rmKpaV1Xrrrrqqtv69gAAAP7VwkNWVd09yQeSvKy7r9tc02VqfRvqK9bdJ3X3wd198O67735rTgUAAFjWQkNWVd0xs4D1ju7+i6l8xXSrX6avV071DUn2njt9rySXbaG+1zL1zV0DAABgoRa5umAleVuSC7r7DXOHPpxkaYXAo5J8aK7+wmmVwUOSXDvd6ndmkqdU1a7TghdPSXLmdOz6qjpkutYLN+pruWsAAAAs1I4L7PtxSV6Q5NyqOmeqvTLJ7yd5b1UdneSSJM+ejp2R5GlJ1if5TpIXJUl3X11Vr0ly9tTu1d199bT9y0lOSbJTko9Nr2zmGgAAAAu1sJDV3Z/J8s9NJcmTlmnfSY7dRF8nJzl5mfq6JA9fpv6N5a4BAACwaFtldUEAAIDthZAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAwkJAFAAAw0IpCVlU9fNEDAQAAWAtWOpP1J1X1+ar6L1W1y0JHBAAAsIqtKGR1979P8vwkeydZV1XvrKqfXejIAAAAVqEVP5PV3RcmeVWS30jyM0lOrKovV9XPL2pwAAAAq81Kn8n6yap6Y5ILkjwxydO7+6HT9hsXOD4AAIBVZccVtntTkrcmeWV3f3ep2N2XVdWrFjIyAACAVWilIetpSb7b3TclSVXdIclduvs73X36wkYHAACwyqz0mayPJ9lpbv+uUw0AAIA5Kw1Zd+nuby3tTNt3XcyQAAAAVq+VhqxvV9VBSztV9cgk391MewAAgO3SSp/JelmS91XVZdP+Hkmes5ghAQAArF4rClndfXZV/dsk/yZJJflyd9+w0JEBAACsQiudyUqSRyXZdzrnEVWV7j5tIaMCAABYpVYUsqrq9CQPSnJOkpumcicRsgAAAOasdCbr4CQHdHcvcjAAAACr3UpXFzwvyf0WORAAAIC1YKUzWbsl+aeq+nyS7y8Vu/sZCxkVAADAKrXSkHXCIgcBAACwVqx0CfdPVdUDkuzf3R+vqrsm2WGxQwMAAFh9VvRMVlX9UpL3J/nTqbRnkr9c1KAAAABWq5UufHFskscluS5JuvvCJPfZ3AlVdXJVXVlV583VTqiqr1XVOdPraXPHfrOq1lfVV6rqqXP1Q6fa+qo6bq6+X1V9rqourKr3VNWdpvqdp/310/F9V/geAQAAfmwrDVnf7+4fLO1U1Y6Z/Z2szTklyaHL1N/Y3QdOrzOm/g5IcmSSh03n/HFV7VBVOyR5c5LDkhyQ5LlT2yT5g6mv/ZNck+ToqX50kmu6+8FJ3ji1AwAA2CpWGrI+VVWvTLJTVf1skvcl+avNndDdn05y9Qr7PzzJu7v7+9391STrkzx6eq3v7oumkPfuJIdXVSV5Yma3MCbJqUmeOdfXqdP2+5M8aWoPAACwcCsNWccluSrJuUlenOSMJK+6jdd8SVV9abqdcNeptmeSS+fabJhqm6rfO8k3u/vGjeo362s6fu3U/haq6piqWldV66666qrb+HYAAAB+ZEUhq7t/2N1v7e5nd/ezpu0t3S64nLckeVCSA5NcnuT1U325maa+DfXN9XXLYvdJ3X1wdx+8++67b27cAAAAK7KiJdyr6qtZJqh09wNvzcW6+4q5Pt+a5CPT7oYke8813SvJZdP2cvWvJ9mlqnacZqvm2y/1tWF6dmznrPy2RQAAgB/LSv8Y8cFz23dJ8uwk97q1F6uqPbr78mn3iCRLKw9+OMk7q+oNSe6fZP8kn89sVmr/qtovydcyWxzjed3dVfXJJM/K7Dmto5J8aK6vo5J8djr+t7dx1g0AAOBWW+kfI/7GRqU/qqrPJPntTZ1TVe9K8vgku1XVhiTHJ3l8VR2Y2azYxZk935XuPr+q3pvkn5LcmOTY7r5p6uclSc7M7I8fn9zd50+X+I0k766q1yb5xyRvm+pvS3J6Va3PbAbryJW8RwAAgBFWervgQXO7d8hsZusemzunu5+7TPlty9SW2r8uyeuWqZ+R2UIbG9cvymz1wY3r38tspg0AAGCrW+ntgq+f274xs1mo/zx8NAAAAKvcSm8XfMKiBwIAALAWrPR2wV/d3PHufsOY4QAAAKxut2Z1wUdltnJfkjw9yadz8z8UDAAAsN1bacjaLclB3X19klTVCUne192/uKiBAQAArEZ3WGG7fZL8YG7/B0n2HT4aAACAVW6lM1mnJ/l8VX0ws79xdUSS0xY2KgAAgFVqpasLvq6qPpbkP0ylF3X3Py5uWAAAAKvTSm8XTJK7Jrmuu/+fJBuqar8FjQkAAGDVWlHIqqrjk/xGkt+cSndM8vZFDQoAAGC1WulM1hFJnpHk20nS3ZcluceiBgUAALBarTRk/aC7O7NFL1JVd1vckAAAAFavlYas91bVnybZpap+KcnHk7x1ccMCAABYnVa6uuB/r6qfTXJdkn+T5Le7+6yFjgwAAGAV2mLIqqodkpzZ3U9OIlgBAABsxhZvF+zum5J8p6p23grjAQAAWNVWdLtgku8lObeqzsq0wmCSdPdLFzIqAACAVWqlIeuj0wsAAIDN2GzIqqp9uvuS7j51aw0IAABgNdvSM1l/ubRRVR9Y8FgAAABWvS2FrJrbfuAiBwIAALAWbClk9Sa2AQAAWMaWFr74qaq6LrMZrZ2m7Uz73d33XOjoAAAAVpnNhqzu3mFrDQQAAGAt2OIfIwYAAGDlhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBhCwAAICBFhayqurkqrqyqs6bq92rqs6qqgunr7tO9aqqE6tqfVV9qaoOmjvnqKn9hVV11Fz9kVV17nTOiVVVm7sGAADA1rDImaxTkhy6Ue24JJ/o7v2TfGLaT5LDkuw/vY5J8pZkFpiSHJ/kMUkeneT4udD0lqnt0nmHbuEaAAAAC7ewkNXdn05y9Ublw5OcOm2fmuSZc/XTeuYfkuxSVXskeWqSs7r76u6+JslZSQ6djt2zuz/b3Z3ktI36Wu4aAAAAC7e1n8m6b3dfniTT1/tM9T2TXDrXbsNU21x9wzL1zV0DAABg4W4vC1/UMrW+DfVbd9GqY6pqXVWtu+qqq27t6QAAALewtUPWFdOtfpm+XjnVNyTZe67dXkku20J9r2Xqm7vGLXT3Sd19cHcfvPvuu9/mNwUAALBka4esDydZWiHwqCQfmqu/cFpl8JAk1063+p2Z5ClVteu04MVTkpw5Hbu+qg6ZVhV84UZ9LXcNAACAhdtxUR1X1buSPD7JblW1IbNVAn8/yXur6ugklyR59tT8jCRPS7I+yXeSvChJuvvqqnpNkrOndq/u7qXFNH45sxUMd0rysemVzVwDAABg4RYWsrr7uZs49KRl2naSYzfRz8lJTl6mvi7Jw5epf2O5awAAAGwNt5eFLwAAANYEIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGAgIQsAAGCgbRKyquriqjq3qs6pqnVT7V5VdVZVXTh93XWqV1WdWFXrq+pLVXXQXD9HTe0vrKqj5uqPnPpfP51bW/9dAgAA26NtOZP1hO4+sLsPnvaPS/KJ7t4/ySem/SQ5LMn+0+uYJG9JZqEsyfFJHpPk0UmOXwpmU5tj5s47dPFvBwAA4PZ1u+DhSU6dtk9N8sy5+mk98w9JdqmqPZI8NclZ3X11d1+T5Kwkh07H7tndn+3uTnLaXF8AAAALta1CVif5m6r6QlUdM9Xu292XJ8n09T5Tfc8kl86du2Gqba6+YZk6AADAwu24ja77uO6+rKruk+SsqvryZtou9zxV34b6LTueBbxjkmSfffbZ/IgBAABWYJvMZHX3ZdPXK5N8MLNnqq6YbvXL9PXKqfmGJHvPnb5Xksu2UN9rmfpy4zipuw/u7oN33333H/dtAQAAbP2QVVV3q6p7LG0neUqS85J8OMnSCoFHJfnQtP3hJC+cVhk8JMm10+2EZyZ5SlXtOi148ZQkZ07Hrq+qQ6ZVBV841xcAAMBCbYvbBe+b5IPTquo7Jnlnd/91VZ2d5L1VdXSSS5I8e2p/RpKnJVmf5DtJXpQk3X11Vb0mydlTu1d399XT9i8nOSXJTkk+Nr0AAAAWbquHrO6+KMlPLVP/RpInLVPvJMduoq+Tk5y8TH1dkof/2IMFAAC4lW5PS7gDAACsekIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQEIWAADAQGs2ZFXVoVX1lapaX1WtcAPUAAAF6UlEQVTHbevxAAAA24c1GbKqaockb05yWJIDkjy3qg7YtqMCAAC2B2syZCV5dJL13X1Rd/8gybuTHL6NxwQAAGwHdtzWA1iQPZNcOre/IcljttFYAIDb6oSdt/UI4PbjhGu39QhYobUasmqZWt+iUdUxSY6Zdr9VVV9Z6Khgddgtyde39SC2d/UH23oEADfjZ8Ptwe8s9ysuW9kDVtJorYasDUn2ntvfK8llGzfq7pOSnLS1BgWrQVWt6+6Dt/U4ALj98LMBbp21+kzW2Un2r6r9qupOSY5M8uFtPCYAAGA7sCZnsrr7xqp6SZIzk+yQ5OTuPn8bDwsAANgOrMmQlSTdfUaSM7b1OGAVcgstABvzswFuheq+xXoQAAAA3EZr9ZksAACAbULIgjWkqrqqXj+3/2tVdcJWHsMpVfWsrXlNAFamqm6qqnPmXvsu4Br7VtV5o/uF1UTIgrXl+0l+vqp2uy0nV9WafU4TgCTJd7v7wLnXxfMH/RyAMfwPCdaWGzN7OPnlSf7r/IGqekCSk5PsnuSqJC/q7kuq6pQkVyd5RJIvVtX1SfZLskeShyT51SSHJDksydeSPL27b6iq307y9CQ7Jfn7JC9uD3kCrDpV9QtJfi7JXZLcraqekeRDSXZNcsckr+ruD02zXh/p7odP5/1akrt39wlV9cjMfsZ8J8lntvqbgNsZM1mw9rw5yfOraueN6m9Kclp3/2SSdyQ5ce7YQ5I8ubtfMe0/KLMfuIcneXuST3b3TyT57lRPkjd196OmH7Y7JfmPC3k3AIy009ytgh+cqz82yVHd/cQk30tyRHcflOQJSV5fVbWFfv88yUu7+7GLGTasLkIWrDHdfV2S05K8dKNDj03yzmn79CT/fu7Y+7r7prn9j3X3DUnOzexvzf31VD83yb7T9hOq6nNVdW6SJyZ52LA3AcCizN8ueMRc/azuvnrariS/W1VfSvLxJHsmue+mOpz+UW+X7v7UVDp9EQOH1cTtgrA2/VGSL2b2L4ubMn9r37c3Ovb9JOnuH1bVDXO3Af4wyY5VdZckf5zk4O6+dFpc4y5DRg7AtjD/c+D5md1a/sjp9vCLM/v/+Btz83+gX/r//crNf6bAds9MFqxB079GvjfJ0XPlv09y5LT9/Px498wv/WD9elXdPYnVBAHWjp2TXDkFrCckecBUvyLJfarq3lV150y3iXf3N5NcW1VLd0g8f6uPGG5nzGTB2vX6JC+Z239pkpOr6tczLXxxWzvu7m9W1Vszu33w4iRn/xjjBOD25R1J/qqq1iU5J8mXk2QKXa9O8rkkX12qT16U2c+Y7yQ5cyuPF253ymJgAAAA47hdEAAAYCAhCwAAYCAhCwAAYCAhCwAAYCAhCwAAYCAhC4DtRlXdr6reXVX/XFX/VFVnVNVDquq8bT02ANYOfycLgO1CVVWSDyY5tbuPnGoHJrnvNh0YAGuOmSwAthdPSHJDd//JUqG7z0ly6dJ+Ve1bVf9vVX1xev27qb5HVX26qs6pqvOq6j9U1Q5Vdcq0f25VvXzrvyUAbo/MZAGwvXh4ki9soc2VSX62u79XVfsneVeSg5M8L8mZ3f26qtohyV2THJhkz+5+eJJU1S6LGzoAq4mQBQA/csckb5puI7wpyUOm+tlJTq6qOyb5y+4+p6ouSvLAqvofST6a5G+2yYgBuN1xuyAA24vzkzxyC21enuSKJD+V2QzWnZKkuz+d5KeTfC3J6VX1wu6+Zmr3d0mOTfJnixk2AKuNkAXA9uJvk9y5qn5pqVBVj0rygLk2Oye5vLt/mOQFSXaY2j0gyZXd/dYkb0tyUFXtluQO3f2BJL+V5KCt8zYAuL1zuyAA24Xu7qo6IskfVdVxSb6X5OIkL5tr9sdJPlBVz07yySTfnuqPT/LrVXVDkm8leWGSPZP8eVUt/YPlby78TQCwKlR3b+sxAAAArBluFwQAABhIyAIAABhIyAIAABhIyAIAABhIyAIAABhIyAIAABhIyAIAABhIyAIAABjo/wdcHD7sZbMKQgAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 1008x576 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "count_classes = pd.value_counts(data['Class'], sort = True)\n",
    "\n",
    "count_classes.plot(kind = 'bar', rot=0)\n",
    "\n",
    "plt.title(\"Transaction Class Distribution\")\n",
    "\n",
    "plt.xticks(range(2), LABELS)\n",
    "\n",
    "plt.xlabel(\"Class\")\n",
    "\n",
    "plt.ylabel(\"Frequency\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Get the Fraud and the normal dataset \n",
    "\n",
    "fraud = data[data['Class']==1]\n",
    "\n",
    "normal = data[data['Class']==0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(492, 31) (284315, 31)\n"
     ]
    }
   ],
   "source": [
    "print(fraud.shape,normal.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "from imblearn.under_sampling import NearMiss"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Implementing Undersampling for Handling Imbalanced \n",
    "nm = NearMiss(random_state=42)\n",
    "X_res,y_res=nm.fit_sample(X,Y)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((984, 30), (984,))"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X_res.shape,y_res.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Original dataset shape Counter({0: 284315, 1: 492})\n",
      "Resampled dataset shape Counter({0: 492, 1: 492})\n"
     ]
    }
   ],
   "source": [
    "\n",
    "\n",
    "from collections import Counter\n",
    "print('Original dataset shape {}'.format(Counter(Y)))\n",
    "print('Resampled dataset shape {}'.format(Counter(y_res)))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
