# 🧪 Manual Testing Guide - Django Statistical Analysis Dashboard

## 📋 Testing Checklist

### ✅ Step 1: Access the Application
1. **Open your web browser**
2. **Navigate to:** http://127.0.0.1:8000/ or http://localhost:8000/
3. **Expected Result:** You should see the Statistical Analysis Dashboard

**✅ PASS** - Dashboard loads successfully  
**❌ FAIL** - Page doesn't load (check server is running)

---

### ✅ Step 2: Check Dashboard Interface
Look for these elements on the page:

**Left Sidebar:**
- [ ] Analysis Configuration panel
- [ ] Data source selection (Radio buttons: Random Data, Upload CSV, Tumor Dataset)
- [ ] Sample size input (for random data)
- [ ] Column selection dropdown
- [ ] Color selection
- [ ] Number of bins slider
- [ ] Checkboxes for showing plots/stats/correlation
- [ ] "Update Analysis" button
- [ ] Dataset information card

**Main Content Area:**
- [ ] Navigation tabs: Visualizations, Statistics, Data Preview
- [ ] Welcome message and description

**✅ PASS** - All interface elements present  
**❌ FAIL** - Missing elements (note which ones)

---

### ✅ Step 3: Test Data Sources

#### 3A: Random Data (Default)
1. **Select "Random Data"** (should be selected by default)
2. **Click "Update Analysis"**
3. **Wait for page to reload**
4. **Check Dataset Information card shows:**
   - Rows: 1000
   - Columns: 3
   - Numeric columns: 3

**✅ PASS** - Random data loads correctly  
**❌ FAIL** - Data doesn't load or shows errors

#### 3B: Tumor Dataset
1. **Select "Tumor Dataset"**
2. **Click "Update Analysis"**
3. **Wait for page to reload**
4. **Check Dataset Information card shows:**
   - Rows: (actual number from dataset)
   - Columns: (actual number from dataset)

**✅ PASS** - Tumor dataset loads correctly  
**❌ FAIL** - Data doesn't load (check if brain_tumor_dataset.csv exists)

---

### ✅ Step 4: Test Visualization Tab (MAIN FOCUS)

1. **Click on "Visualizations" tab** (should be active by default)
2. **Wait for plots to load** (you'll see loading spinners)
3. **Check each plot area:**

#### Distribution Plot (Histogram)
- [ ] Shows a histogram chart
- [ ] Has proper title and axis labels
- [ ] Data appears to be plotted correctly

**✅ PASS** - Distribution plot displays correctly  
**❌ FAIL** - Plot is empty or shows error

#### Box Plot
- [ ] Shows a box plot
- [ ] Has proper title and axis labels
- [ ] Shows quartiles and outliers

**✅ PASS** - Box plot displays correctly  
**❌ FAIL** - Plot is empty or shows error

#### Q-Q Plot
- [ ] Shows a Q-Q plot with scattered points
- [ ] Has reference line
- [ ] Proper axis labels

**✅ PASS** - Q-Q plot displays correctly  
**❌ FAIL** - Plot is empty or shows error

#### Correlation Matrix
- [ ] Shows a heatmap
- [ ] Has correlation values displayed
- [ ] Color-coded correlation strength

**✅ PASS** - Correlation plot displays correctly  
**❌ FAIL** - Plot is empty or shows error

---

### ✅ Step 5: Test Statistics Tab

1. **Click on "Statistics" tab**
2. **Wait for statistics to load**
3. **Check the following sections:**

#### Summary Statistics Card
- [ ] Shows Mean, Std Dev, Median, Count
- [ ] Values are numerical and reasonable

#### Hypothesis Test Card
- [ ] Shows t-statistic and p-value
- [ ] Shows test result (Reject/Fail to reject H₀)
- [ ] Shows normality test result

#### Distribution Details Table
- [ ] Shows detailed statistics table
- [ ] Two columns with various statistics
- [ ] All values are numerical

**✅ PASS** - Statistics display correctly  
**❌ FAIL** - Statistics missing or show errors

---

### ✅ Step 6: Test Data Preview Tab

1. **Click on "Data Preview" tab**
2. **Wait for data to load**
3. **Check the data table:**

- [ ] Shows first 100 rows of data
- [ ] Has column headers
- [ ] Data values appear reasonable
- [ ] Shows "Showing X of Y rows" message

**✅ PASS** - Data preview displays correctly  
**❌ FAIL** - Data preview missing or shows errors

---

### ✅ Step 7: Test Interactive Features

#### Column Selection
1. **Go back to Visualizations tab**
2. **In the sidebar, change the selected column**
3. **Click "Update Analysis"**
4. **Check if plots update with new column data**

**✅ PASS** - Column selection works correctly  
**❌ FAIL** - Plots don't update or show errors

#### Bin Size Adjustment
1. **Change the "Number of bins" slider**
2. **Click "Update Analysis"**
3. **Check if histogram updates with different bin count**

**✅ PASS** - Bin adjustment works correctly  
**❌ FAIL** - Histogram doesn't change

#### Color Selection
1. **Change the color dropdown**
2. **Click "Update Analysis"**
3. **Check if histogram color changes**

**✅ PASS** - Color selection works correctly  
**❌ FAIL** - Plot color doesn't change

---

### ✅ Step 8: Test Quick Actions

1. **Click "Refresh Plots" button**
2. **Check if plots reload**
3. **Click "Refresh All" button**
4. **Check if all tabs reload**

**✅ PASS** - Refresh buttons work correctly  
**❌ FAIL** - Refresh doesn't work

---

## 🔍 Debugging Empty Distribution Plot

If the **Distribution Plot (Histogram) is empty**, check:

1. **Browser Console** (Press F12, go to Console tab):
   - Look for JavaScript errors
   - Look for failed network requests

2. **Django Server Terminal**:
   - Look for debug messages starting with "DEBUG get_plots:"
   - Look for debug messages starting with "DEBUG create_histogram_plotly:"

3. **Common Issues:**
   - Selected column might not exist in data
   - Column might not be numeric
   - Data might be empty or contain only null values

---

## 📊 Expected Results Summary

**With Random Data:**
- Histogram: Should show normal distribution
- Box plot: Should show quartiles and possible outliers
- Q-Q plot: Should show points roughly following diagonal line
- Correlation matrix: Should show correlation between X, Y, Z columns

**With Tumor Dataset:**
- Plots will vary based on the actual dataset content
- Should show realistic medical data distributions

---

## 🆘 Troubleshooting

### If Dashboard Doesn't Load:
1. Check if Django server is running
2. Verify URL: http://127.0.0.1:8000/
3. Check terminal for server errors

### If Plots Are Empty:
1. Check browser console for JavaScript errors
2. Check Django server terminal for debug output
3. Try switching between data sources
4. Try different columns

### If Statistics Don't Load:
1. Check if data source is working
2. Verify column selection is valid
3. Check server terminal for errors

---

## ✅ Success Criteria

**Minimum Requirements:**
- ✅ Dashboard loads successfully
- ✅ At least one data source works
- ✅ At least histogram shows data
- ✅ Statistics tab shows summary data
- ✅ Data preview shows table

**Full Success:**
- ✅ All data sources work
- ✅ All four plot types display correctly
- ✅ All statistics display correctly
- ✅ Interactive features work (column selection, bins, colors)
- ✅ No errors in browser console or server terminal

---

**�� Happy Testing!** 