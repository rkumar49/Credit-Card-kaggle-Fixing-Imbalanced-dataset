{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
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
   "execution_count": 2,
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
     "execution_count": 2,
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
   "execution_count": 3,
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
   "execution_count": 5,
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
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "False"
      ]
     },
     "execution_count": 6,
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
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Text(0, 0.5, 'Frequency')"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAZsAAAEWCAYAAACwtjr+AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDMuMC4yLCBodHRwOi8vbWF0cGxvdGxpYi5vcmcvOIA7rQAAHUFJREFUeJzt3Xu8VXWd//HXO0DFOwoqAgYqzoQ2IeItZyZvKdoo2uik+VPyZ+GvwYej2YzkVJJp5a/MfoxlYRIX75dMK4zQTH+WKUdjBG9xUhSEBAUB74Cf+WN9dy4O+5yzD5zv2bh5Px+P/ThrfdZ3fdd3rX3O/uz1Xd+zliICMzOznD5Q7waYmVnjc7IxM7PsnGzMzCw7JxszM8vOycbMzLJzsjEzs+ycbMxKJB0q6Yk6bftBSZ+px7arkdRN0muSduuk+r4i6Ydpek9JnfZ/F5J2l/RaZ9Vnnc/JxtZb+iCqvN6V9GZp/rR6t689krpLCkkDK7GI+G1E7J1pe5tLukRSs6TXJc2T9OPO+jDvYFuOTO9Z5f1aIOlmSftVykTEmojYOiJeqKGuee1tMyK+HhH/pxOaT2rvoaW6n42IrTujbsvDycbWW/og2jr9kb8AHFeKXd+yvKTuXd/KjYMkAT8FjgE+BWwHDAUeBw6vU7NeSO/dNsDBQDPwu/KHeGfZlN97KzjZWDaSLk3flm+UtBL4X5IOlvQHSa9KWiRpvKQeqXzlTOPs9O1/maTxpfr2kvSApOWSXpZ0Q2nZVenb7gpJMyV9tLSse+rC+XNa3iRpV+CBVOSJ9O3+n1t+S5e0t6T7U3tnS/pEadl1qf13S1op6SFJg1o5HEcDhwEnRMSjEbE6Il6NiPERManKsRss6T5Jr6R9nSppu9LyiyQtTPvzdCVBSDpI0mMp/pKkb7f3PkVhfkT8JzAJ+FaL92Ngmv8nSU+lfV0g6fzUpp8Du5XOknZq5b2/VNJa+yrpc2k/Fko6v8WxHVea/+v7IulGYFfg7rS9L6hFt5yk/pJ+IWmppLmS/ndp2aWpXdelfZkjaVh7x8k2UET45dcGv4B5wJEtYpcC7wDHUXyx6QnsDxwIdAd2B/4EnJPKdwcCuJPim/9AYGmlXuBW4MJU1xbAIaVtnQ7skOq4EHgR2Dwt+xLw38DgtO7QUtkABpbqORKYl6Y3A54D/gPokZa9BuyZll8HvAwMT8tvBq5r5fh8B7i3nWP4IPCZNL0XcERqw07A74DvpGV7A88Du6T5QcDuaXomcGqa3gY4sJVt/XU/W8SPAtak47vW8QGWAB9N0zsAw1qrq5X3/lJgUlq+Z6p7KrAl8BHgFeDQ0rEd11p7gQWVsuX6SvO/A/4r7cew9D59rNS2Nym+AHQDvg08WO+/oUZ/+czGcnswIn4eEe9GxJsRMTMiHo7im/2zwATgYy3W+WZELI+IecBvKZIDwCqKBNQ3It6KiN9VVoiIqRGxNCJWA/8X2JbiAwjgs8BFETE3tWNWRCytoe2HUHzYfzsiVkXEPcDdwCmlMrdFRFNErAKuL7W1pR2BRTVss7I/f4qIeyPinYhYDFzJe8dpNcWH6N6SukfEc+lYQnGMBkvaMSJWRsTDtW4zWUiRHLarsmwVMETSNulYP9ZOXWu9962U+VpEvBER/w1MBk7tYHvXkc4uDwDGpt+Tx4CfUHwhqbg/IqZHxBqKhNfa+2adxMnGcptfnpH0t5J+KekvklYAlwC9W6zzl9L0G0Dlwu8FFGcQTalLa1Sp3v9I3UnLgWXAVqV6BwB/Xo+270pxXaM8aup5oF8NbW3pFaBvrRuWtIukWyS9mI7TJNL+RMQzFMfiEmBx6hLaJa16JjAEeEbSI5KOrXWbST/gXWB5lWUnAscDL0j6raQD26lrfjvLW5Z5nuKYb6hdgZcj4vUWdbf1vm3VCdu1NjjZWG4th7f+CJhD0RW1LfBVQDVVFLEoIj4bEX2BMcAESYMkHQZ8AfhnYHugF0V3V6Xe+cAeNbStpYXAAEnl9u1G0UXXUfcAB6drRbW4HHgb+HA6Tp+hdJwi4rqIOISiC60b8M0UfyYiTqHoersCuF3SFh1o54nAzIh4q+WCdEZ6fKr7F8BNlUWt1FXL0OYBpendKI45wOsU3WsVu7C2tupeCPSWVE4g6/u+WSdxsrGutg3Ft+bXJX0IOLvWFSX9i6TKt9NXKT5w1qQ6V1P0y/cAxrH2N9UfA5dK2kOFoZJ2SF0or1BcO6rm96neCyT1kHQ4cCxwS61tLpkO3AfcIWlfFf/Dsq2kfy2foZVsQ/GBu1zSAOCLpePwIUmHSdqc4trDm+k4IOl0Sb0jonJ2EhRnKq1Kx6S/pK9RJLWLqpTpKenTkrZNXYYrK9sEXqL4cN+mA8ej4iup7g8DoyiuewHMAj4hqZekvsC5LdZ7iVbet4h4DmgCvqFiuPlQijO+dUZIWtdxsrGudgHFh8pKirOcm9suvpYDgZmSXqcYRjwmiv8BmUZx5jCXYqDCCta+PvJt4GfAvWnZBIprHgAXAzeoGG32yfLGIuJtigvcIykS2Xjg0xHxpw60uVJXAJ8Efg3cltoxm+JawW+qrHIxxXWH5cBdwO2lZZtTXJd6maI7qBfw5bTsWOCpNALsO8CnIuKdVpq1m4p/hHwNeJii++0fI6Jae6B4355P3Xpnka6BRMSc1L556Tju1MahaOlB4FmK4/LN0rYnAU9RdH/9ivfOoiq+AXwtbe+8KvV+imJAyF8ojvdFEXFfB9plnUxrd0ebmZl1Pp/ZmJlZdk42ZmaWnZONmZll52RjZmbZ+eZ4Se/evWPgwIH1boaZ2fvKo48++nJE9GmvnJNNMnDgQJqamurdDDOz9xVJz9dSzt1oZmaWnZONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp3vIPA+M3DsL+vdhIYy71ufqHcTzDYJPrMxM7PsnGzMzCw7JxszM8vOycbMzLJzsjEzs+ycbMzMLDsnGzMzy87JxszMsnOyMTOz7JxszMwsOycbMzPLzsnGzMyyc7IxM7PsnGzMzCw7JxszM8vOycbMzLJzsjEzs+ycbMzMLDsnGzMzy87JxszMsnOyMTOz7LIlG0kDJN0n6SlJT0j6txQfJ+lFSbPS69jSOl+S1CzpGUlHl+IjUqxZ0thSfJCkhyXNlXSzpM1SfPM035yWD8y1n2Zm1r6cZzargQsi4kPAQcAYSUPSsisjYmh6TQNIy04B9gZGAD+Q1E1SN+D7wDHAEODUUj2Xp7oGA8uAs1L8LGBZROwJXJnKmZlZnWRLNhGxKCIeS9MrgaeAfm2sMhK4KSLejojngGbggPRqjohnI+Id4CZgpCQBhwO3pfUnAyeU6pqcpm8DjkjlzcysDrrkmk3qxtoXeDiFzpH0uKSJknqlWD9gfmm1BSnWWnxH4NWIWN0ivlZdafnyVL5lu0ZLapLUtGTJkg3aRzMza132ZCNpa+B24LyIWAFcDewBDAUWAVdUilZZPdYj3lZdawciJkTE8IgY3qdPnzb3w8zM1l/WZCOpB0WiuT4ifgoQES9FxJqIeBe4hqKbDIozkwGl1fsDC9uIvwxsL6l7i/hadaXl2wFLO3fvzMysVjlHowm4FngqIr5bivctFTsRmJOm7wJOSSPJBgGDgUeAmcDgNPJsM4pBBHdFRAD3ASel9UcBd5bqGpWmTwJ+k8qbmVkddG+/yHo7BDgdmC1pVopdRDGabChFt9Y84GyAiHhC0i3AkxQj2cZExBoASecA04FuwMSIeCLVdyFwk6RLgT9SJDfSz6mSminOaE7JuJ9mZtaObMkmIh6k+rWTaW2scxlwWZX4tGrrRcSzvNcNV46/BZzckfaamVk+voOAmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp2TjZmZZedkY2Zm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp2TjZmZZedkY2Zm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZOdmYmVl22ZKNpAGS7pP0lKQnJP1biu8gaYakuelnrxSXpPGSmiU9LmlYqa5RqfxcSaNK8f0kzU7rjJektrZhZmb1kfPMZjVwQUR8CDgIGCNpCDAWuDciBgP3pnmAY4DB6TUauBqKxAFcDBwIHABcXEoeV6eylfVGpHhr2zAzszrIlmwiYlFEPJamVwJPAf2AkcDkVGwycEKaHglMicIfgO0l9QWOBmZExNKIWAbMAEakZdtGxEMREcCUFnVV24aZmdVBl1yzkTQQ2Bd4GNg5IhZBkZCAnVKxfsD80moLUqyt+IIqcdrYRst2jZbUJKlpyZIl67t7ZmbWjuzJRtLWwO3AeRGxoq2iVWKxHvGaRcSEiBgeEcP79OnTkVXNzKwDsiYbST0oEs31EfHTFH4pdYGRfi5O8QXAgNLq/YGF7cT7V4m3tQ0zM6uDnKPRBFwLPBUR3y0tuguojCgbBdxZip+RRqUdBCxPXWDTgaMk9UoDA44CpqdlKyUdlLZ1Rou6qm3DzMzqoHvGug8BTgdmS5qVYhcB3wJukXQW8AJwclo2DTgWaAbeAM4EiIilkr4OzEzlLomIpWn688AkoCdwd3rRxjbMzKwOsiWbiHiQ6tdVAI6oUj6AMa3UNRGYWCXeBOxTJf5KtW2YmVl9+A4CZmaWnZONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtnVlGwkrfO/LGZmZrWq9czmh5IekfSvkrbP2iIzM2s4NSWbiPh74DSKG2I2SbpB0seztszMzBpGzddsImIu8GXgQuBjwHhJT0v6ZK7GmZlZY6j1ms3fSbqS4mmbhwPHpcc9Hw5cmbF9ZmbWAGq9EedVwDXARRHxZiUYEQslfTlLy8zMrGHUmmyOBd6MiDUAkj4AbBERb0TE1GytMzOzhlDrNZt7KJ4ZU7FlipmZmbWr1mSzRUS8VplJ01vmaZKZmTWaWpPN65KGVWYk7Qe82UZ5MzOzv6r1ms15wK2SFqb5vsCn8jTJzMwaTU3JJiJmSvpb4G8oHvX8dESsytoyMzNrGLWe2QDsDwxM6+wriYiYkqVVZmbWUGpKNpKmAnsAs4A1KRyAk42ZmbWr1jOb4cCQiIicjTEzs8ZU62i0OcAuORtiZmaNq9Yzm97Ak5IeAd6uBCPi+CytMjOzhlJrshmXsxFmZtbYah36fL+kDwKDI+IeSVsC3fI2zczMGkWtjxj4HHAb8KMU6gf8LFejzMyssdQ6QGAMcAiwAv76ILWd2lpB0kRJiyXNKcXGSXpR0qz0Ora07EuSmiU9I+noUnxEijVLGluKD5L0sKS5km6WtFmKb57mm9PygTXuo5mZZVJrsnk7It6pzEjqTvF/Nm2ZBIyoEr8yIoam17RU3xDgFGDvtM4PJHWT1A34PnAMMAQ4NZUFuDzVNRhYBpyV4mcByyJiT4oHu11e4z6amVkmtSab+yVdBPSU9HHgVuDnba0QEQ8AS2usfyRwU0S8HRHPAc3AAenVHBHPpmR3EzBSkiieEnpbWn8ycEKprslp+jbgiFTezMzqpNZkMxZYAswGzgamAev7hM5zJD2eutl6pVg/YH6pzIIUay2+I/BqRKxuEV+rrrR8eSpvZmZ1UlOyiYh3I+KaiDg5Ik5K0+tzN4GrKW57MxRYBFyR4tXOPGI94m3VtQ5JoyU1SWpasmRJW+02M7MNUOu90Z6jygd2ROzekY1FxEulOq8BfpFmFwADSkX7A5XHGVSLvwxsL6l7Onspl6/UtSBdW9qOVrrzImICMAFg+PDhvhWPmVkmHbk3WsUWwMnADh3dmKS+EbEozZ5IcRscgLuAGyR9F9gVGAw8QnGWMljSIOBFikEEn46IkHQfcBLFdZxRwJ2lukYBD6Xlv/E93czM6qvWf+p8pUXoe5IeBL7a2jqSbgQOBXpLWgBcDBwqaSjFWdI8ius/RMQTkm4BngRWA2MiYk2q5xxgOsU/kU6MiCfSJi4EbpJ0KfBH4NoUvxaYKqmZ4ozmlFr20czM8qm1G21YafYDFGc627S1TkScWiV8bZVYpfxlwGVV4tMoBiS0jD9LMVqtZfwtijMvMzPbSNTajXZFaXo1xVnJv3R6a8zMrCHV2o12WO6GmJlZ46q1G+0LbS2PiO92TnPMzKwRdWQ02v4UI70AjgMeYO1/uDQzM6uqIw9PGxYRK6G4oSZwa0R8NlfDzMyscdR6u5rdgHdK8+8AAzu9NWZm1pBqPbOZCjwi6Q6K/5E5EZiSrVVmZtZQah2Ndpmku4F/SKEzI+KP+ZplZmaNpNZuNIAtgRUR8f8o7js2KFObzMyswdT6WOiLKW4P86UU6gFcl6tRZmbWWGo9szkROB54HSAiFtLO7WrMzMwqak0276Q7JweApK3yNcnMzBpNrcnmFkk/oniGzOeAe4Br8jXLzMwaSa2j0b4j6ePACuBvgK9GxIysLTMzs4bRbrKR1A2YHhFHAk4wZmbWYe12o6WHmL0habsuaI+ZmTWgWu8g8BYwW9IM0og0gIg4N0urzMysodSabH6ZXmZmZh3WZrKRtFtEvBARk7uqQWZm1njau2bzs8qEpNszt8XMzBpUe8lGpendczbEzMwaV3vJJlqZNjMzq1l7AwQ+ImkFxRlOzzRNmo+I2DZr68zMrCG0mWwioltXNcTMzBpXR55nY2Zmtl6cbMzMLDsnGzMzy87JxszMssuWbCRNlLRY0pxSbAdJMyTNTT97pbgkjZfULOlxScNK64xK5edKGlWK7ydpdlpnvCS1tQ0zM6ufnGc2k4ARLWJjgXsjYjBwb5oHOAYYnF6jgauhSBzAxcCBwAHAxaXkcXUqW1lvRDvbMDOzOsmWbCLiAWBpi/BIoHKftcnACaX4lCj8geKJoH2Bo4EZEbE0IpZRPE9nRFq2bUQ8lB5XPaVFXdW2YWZmddLV12x2johFAOnnTineD5hfKrcgxdqKL6gSb2sb65A0WlKTpKYlS5as906ZmVnbNpYBAqoSi/WId0hETIiI4RExvE+fPh1d3czMatTVyeal1AVG+rk4xRcAA0rl+gML24n3rxJvaxtmZlYnXZ1s7gIqI8pGAXeW4mekUWkHActTF9h04ChJvdLAgKOA6WnZSkkHpVFoZ7Soq9o2zMysTmp9UmeHSboROBToLWkBxaiybwG3SDoLeAE4ORWfBhwLNANvAGcCRMRSSV8HZqZyl0REZdDB5ylGvPUE7k4v2tiGmZnVSbZkExGntrLoiCplAxjTSj0TgYlV4k3APlXir1TbhpmZ1c/GMkDAzMwamJONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp2TjZmZZedkY2Zm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp2TjZmZZedkY2Zm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZ1SXZSJonabakWZKaUmwHSTMkzU0/e6W4JI2X1CzpcUnDSvWMSuXnShpViu+X6m9O66rr99LMzCrqeWZzWEQMjYjhaX4scG9EDAbuTfMAxwCD02s0cDUUyQm4GDgQOAC4uJKgUpnRpfVG5N8dMzNrzcbUjTYSmJymJwMnlOJTovAHYHtJfYGjgRkRsTQilgEzgBFp2bYR8VBEBDClVJeZmdVBvZJNAL+W9Kik0Sm2c0QsAkg/d0rxfsD80roLUqyt+IIq8XVIGi2pSVLTkiVLNnCXzMysNd3rtN1DImKhpJ2AGZKebqNstestsR7xdYMRE4AJAMOHD69axszMNlxdzmwiYmH6uRi4g+Kay0upC4z0c3EqvgAYUFq9P7CwnXj/KnEzM6uTLk82kraStE1lGjgKmAPcBVRGlI0C7kzTdwFnpFFpBwHLUzfbdOAoSb3SwICjgOlp2UpJB6VRaGeU6jIzszqoRzfazsAdaTRyd+CGiPiVpJnALZLOAl4ATk7lpwHHAs3AG8CZABGxVNLXgZmp3CURsTRNfx6YBPQE7k4vMzOrky5PNhHxLPCRKvFXgCOqxAMY00pdE4GJVeJNwD4b3FgzM+sUG9PQZzMza1BONmZmlp2TjZmZZedkY2Zm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp2TjZmZZedkY2Zm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZOdmYmVl2TjZmZpadk42ZmWXnZGNmZtk52ZiZWXZONmZmlp2TjZmZZedkY2Zm2TVsspE0QtIzkpolja13e8zMNmUNmWwkdQO+DxwDDAFOlTSkvq0yM9t0da93AzI5AGiOiGcBJN0EjASerGurzBrZuO3q3YLGMm55vVvQqRo12fQD5pfmFwAHtiwkaTQwOs2+JumZLmjbpqI38HK9G9EeXV7vFlgdvC9+N/ma6t2CWn2wlkKNmmyqvUuxTiBiAjAhf3M2PZKaImJ4vdth1pJ/N+ujIa/ZUJzJDCjN9wcW1qktZmabvEZNNjOBwZIGSdoMOAW4q85tMjPbZDVkN1pErJZ0DjAd6AZMjIgn6tysTY27J21j5d/NOlDEOpcyzMzMOlWjdqOZmdlGxMnGzMyyc7KxdUgKSVeU5r8oaVwXt2GSpJO6cpv2/iNpjaRZpdfADNsYKGlOZ9e7qXGysWreBj4pqff6rCypIQee2EbpzYgYWnrNKy/07+LGw2+EVbOaYsTO+cB/lhdI+iAwEegDLAHOjIgXJE0ClgL7Ao9JWgkMAvoCewFfAA6iuF/di8BxEbFK0leB44CewO+Bs8OjVmwDSPoM8AlgC2ArSccDdwK9gB7AlyPiznQW9IuI2Cet90Vg64gYJ2k/it/zN4AHu3wnGpDPbKw13wdOk9TyhldXAVMi4u+A64HxpWV7AUdGxAVpfg+KP/qRwHXAfRHxYeDNFAe4KiL2T3/wPYF/yrI31qh6lrrQ7ijFDwZGRcThwFvAiRExDDgMuEJSe/eC+QlwbkQcnKfZmx4nG6sqIlYAU4BzWyw6GLghTU8F/r607NaIWFOavzsiVgGzKf7f6VcpPhsYmKYPk/SwpNnA4cDenbYTtikod6OdWIrPiIilaVrANyQ9DtxDce/EnVurMH3B2j4i7k+hqTkavqlxN5q15XvAYxTf8lpT7vJ6vcWytwEi4l1Jq0rdY+8C3SVtAfwAGB4R89MghC06peW2qSv/Lp5G0e27X+q6nUfxe7aatb9wV373RJV7KdqG8ZmNtSp9M7wFOKsU/j3F7X+g+CPekP7syh/3y5K2Bjz6zHLYDlicEs1hvHeX4peAnSTtKGlzUhduRLwKLJdUOWs/rctb3IB8ZmPtuQI4pzR/LjBR0r+TBgisb8UR8aqkayi61eZR3NPOrLNdD/xcUhMwC3gaICWfS4CHgecq8eRMit/zNyhue2UbyLerMTOz7NyNZmZm2TnZmJlZdk42ZmaWnZONmZll52RjZmbZOdmY1YGkXSTdJOnPkp6UNE3SXr67sDUq/5+NWRdL9+W6A5gcEaek2FDauIWK2fudz2zMut5hwKqI+GElEBGzgPmV+fQMlf8v6bH0+miK95X0QLrx5BxJ/yCpW3r+zxxJsyWd3/W7ZNY2n9mYdb19gEfbKbMY+HhEvCVpMHAjMBz4NDA9Ii6T1A3YEhgK9CvdKn/7fE03Wz9ONmYbpx7AVal7bQ3F4xuguKXPREk9gJ9FxCxJzwK7S/ov4JfAr+vSYrM2uBvNrOs9AezXTpnzKW4U+RGKM5rNACLiAeAfKR5AN1XSGRGxLJX7LTAG+HGeZputPycbs673G2BzSZ+rBCTtz3t3I4biTsWLIuJd4HSK5wFVnpS6OCKuAa4FhqXHd38gIm4HvgIM65rdMKudu9HMulhEhKQTge9JGkvxJMl5wHmlYj8Abpd0MnAf7z2f5VDg3yWtAl4DzqB4GNhPJFW+PH4p+06YdZDv+mxmZtm5G83MzLJzsjEzs+ycbMzMLDsnGzMzy87JxszMsnOyMTOz7JxszMwsu/8BrC9x23iJiHgAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
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
   "execution_count": 8,
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
   "execution_count": 9,
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
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "from imblearn.combine import SMOTETomek\n",
    "from imblearn.under_sampling import NearMiss"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Implementing Oversampling for Handling Imbalanced \n",
    "smk = SMOTETomek(random_state=42)\n",
    "X_res,y_res=smk.fit_sample(X,Y)\n"
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
       "((567562, 30), (567562,))"
      ]
     },
     "execution_count": 12,
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
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Original dataset shape Counter({0: 284315, 1: 492})\n",
      "Resampled dataset shape Counter({0: 283781, 1: 283781})\n"
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
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "## RandomOverSampler to handle imbalanced data\n",
    "\n",
    "from imblearn.over_sampling import RandomOverSampler"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "metadata": {},
   "outputs": [],
   "source": [
    "os =  RandomOverSampler(ratio=0.5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [],
   "source": [
    "X_train_res, y_train_res = os.fit_sample(X, Y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((426472, 30), (426472,))"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X_train_res.shape,y_train_res.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Original dataset shape Counter({0: 284315, 1: 492})\n",
      "Resampled dataset shape Counter({0: 284315, 1: 142157})\n"
     ]
    }
   ],
   "source": [
    "print('Original dataset shape {}'.format(Counter(Y)))\n",
    "print('Resampled dataset shape {}'.format(Counter(y_train_res)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "metadata": {},
   "outputs": [],
   "source": [
    "# In this example I use SMOTETomek which is a method of imblearn. SMOTETomek is a hybrid method\n",
    "# which uses an under sampling method (Tomek) in with an over sampling method (SMOTE).\n",
    "os_us = SMOTETomek(ratio=0.5)\n",
    "\n",
    "X_train_res1, y_train_res1 = os_us.fit_sample(X, Y)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((424788, 30), (424788,))"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "X_train_res1.shape,y_train_res1.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Original dataset shape Counter({0: 284315, 1: 492})\n",
      "Resampled dataset shape Counter({0: 283473, 1: 141315})\n"
     ]
    }
   ],
   "source": [
    "print('Original dataset shape {}'.format(Counter(Y)))\n",
    "print('Resampled dataset shape {}'.format(Counter(y_train_res1)))"
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
