from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import csv
import pandas
import time

df = pandas.read_csv('user_calories_stats.csv', index_col='User')


chrome_option = Options()


#User info
user_name = input('What is your name? ')



# Check if User already in the csv
user_in = False
update_user = False
user = 0
for n in range(len(df)):
    if user_name in df.index:
        print(f"User already in the database: \n {df.loc[user_name]}")
        answer = input('Do you want update the User data? y/n ').lower()
        delete = input('Do you want to delete this User? y/n ').lower()

        if answer == 'y':
            update_user = True
            user = n

        else:
            user_in = True

        if delete == 'y':
            df = df.drop(user_name)
            df.to_csv('user_calories_stats.csv')


if not user_in:

    # User info
    user_age = int(input("What's your age? "))
    ft_w = input('What metric do you use? U.S. units or International unit? Press "US" or "IU" ').lower()

    user_gender = input('What is your gender "F" or "M"? ').lower()
    activity_level = input('What is your activity level? "Inactive" "Somewhat active" "Active" "Very active"? ').lower()
    # Setting Driver
    chrome_driver_path = Service("/Users/rosariomanzillo/Desktop/Damiano/chromedriver")
    driver = webdriver.Chrome(service=chrome_driver_path, options=chrome_option)

    driver.get('https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/calorie-calculator/itt-20402304')
    time.sleep(3)

    # Check metric
    if ft_w == 'iu':
        switch_metric = driver.find_element(By.CSS_SELECTOR,'#main-content #units')
        switch_metric.click()
        user_weight = int(input("What's your weight? "))
        user_height = int(input("What's your height? "))
        height = driver.find_element(By.CSS_SELECTOR, '#main-content #centimeters')
        height.send_keys(user_height)
        time.sleep(1)
        weight = driver.find_element(By.CSS_SELECTOR, '#main-content #weight')
        weight.send_keys(user_weight)
    else:
        user_weight_lb = int(input("What's your weight lbs? "))
        user_height_ft = int(input("What's your height ft? "))
        user_height_in = int(input("What's your inch? "))
        height = driver.find_element(By.CSS_SELECTOR,'#main-content #feet')
        height.send_keys(user_height_ft)
        time.sleep(1)
        inch = driver.find_element(By.CSS_SELECTOR, '#main-content #inches')
        inch.send_keys(user_height_ft)
        time.sleep(1)
        weight = driver.find_element(By.CSS_SELECTOR,'#main-content #weight')
        weight.send_keys(user_weight_lb)

    age = driver.find_element(By.CSS_SELECTOR,'#main-content #age')
    age.send_keys(user_age)
    time.sleep(1)
    # Check gender
    if user_gender == 'm':
        gender_male = driver.find_element(By.CSS_SELECTOR,'#main-content #male')
        gender_male.click()
    else:
        gender_female = driver.find_element(By.CSS_SELECTOR, '#main-content #female')
        gender_female.click()

    time.sleep(1)

    results = driver.find_element(By.XPATH,'//*[@id="calorieCalculator"]/div/button[2]')
    results.click()
    time.sleep(3)

    # Check activity level

    if activity_level == 'active':
        daily_activity = driver.find_element(By.CSS_SELECTOR,'#main-content #active')
        daily_activity.click()
        time.sleep(3)
    elif activity_level == 'inactive':
        daily_activity = driver.find_element(By.CSS_SELECTOR, '#main-content #inactive')
        daily_activity.click()
        time.sleep(3)
    elif activity_level == 'somewhat active':
        daily_activity = driver.find_element(By.CSS_SELECTOR, '#main-content #somewhat-active')
        daily_activity.click()
        time.sleep(3)
    else:
        daily_activity = driver.find_element(By.CSS_SELECTOR, '#main-content #very-active')
        daily_activity.click()
        time.sleep(3)




    calculate = driver.find_element(By.CSS_SELECTOR,'#main-content .submit')
    calculate.click()
    time.sleep(3)

    if activity_level == 'active':
        user_daily_calories = driver.find_element(By.XPATH,'/html/body/form/div[5]/div[2]/div[5]/div/div/div[2]/div[2]/div[2]/ul/li[3]/a/span[1]')
        user_daily_calories = int(user_daily_calories.text)

        time.sleep(3)
    elif activity_level == 'inactive':
        user_daily_calories = driver.find_element(By.XPATH,'/html/body/form/div[5]/div[2]/div[5]/div/div/div[2]/div[2]/div[2]/ul/li[1]/a/span[1]')
        user_daily_calories = int(user_daily_calories.text)

        time.sleep(3)
    elif activity_level == 'somewhat active':
        user_daily_calories = driver.find_element(By.XPATH, '/html/body/form/div[5]/div[2]/div[5]/div/div/div[2]/div[2]/div[2]/ul/li[2]/a/span[1]')
        user_daily_calories = int(user_daily_calories.text)

        time.sleep(3)
    elif activity_level == 'very active':
        user_daily_calories = driver.find_element(By.XPATH,'/html/body/form/div[5]/div[2]/div[5]/div/div/div[2]/div[2]/div[2]/ul/li[4]/a/span[1]')
        user_daily_calories = int(user_daily_calories.text)

        time.sleep(3)


    mild_weight_loss = (user_daily_calories * 91) /100
    weight_loss = (user_daily_calories * 83) / 100
    extreme_weight_loss = (user_daily_calories * 63) / 100
    mild_weight_gain =(user_daily_calories * 109) / 100
    weight_gain = (user_daily_calories * 118) / 100
    fast_weight_gain = (user_daily_calories * 137) / 100

    if update_user:
        df.loc[user,'User'] = user_name
        df.loc[user,'Calories'] = user_daily_calories
        df.loc[user,'Maintain Weight(100%)'] = user_daily_calories
        df.loc[user, 'Mild Weight Loss(91%)'] = mild_weight_loss
        df.loc[user, 'Weight Loss(82%)'] = weight_loss
        df.loc[user, 'Extreme Weight Loss(63%)'] =extreme_weight_loss
        df.loc[user, 'Mild Weight Gain(109%)'] = mild_weight_gain
        df.loc[user, 'Weight Gain(118%)'] = weight_gain
        df.loc[user, 'Fast Weight Gain(137%)'] = fast_weight_gain
        df.to_csv('user_calories_stats.csv', index=False)
        print(df.loc[user])


    else:
        with open('user_calories_stats.csv', 'a', newline='') as file:
            columns = ['User', 'Calories', 'Maintain Weight(100%)', 'Mild Weight Loss(91%)', 'Weight Loss(82%)', 'Extreme Weight Loss(63%)', 'Mild Weight Gain(109%)',
                       'Weight Gain(118%)', 'Fast Weight Gain(137%)']
            write = csv.DictWriter(file, fieldnames=columns)

            write.writerow({'User':user_name,'Calories':user_daily_calories,  'Maintain Weight(100%)':user_daily_calories, 'Mild Weight Loss(91%)':mild_weight_loss,
                            'Weight Loss(82%)':weight_loss, 'Extreme Weight Loss(63%)':extreme_weight_loss, 'Mild Weight Gain(109%)':mild_weight_gain,
                            'Weight Gain(118%)':weight_gain, 'Fast Weight Gain(137%)':fast_weight_gain})

        df = pandas.read_csv('user_calories_stats.csv')

        for n in range(len(df)):
            if user_name == df['User'][n]:
                print(f'Today: {datetime.today().strftime("%Y-%m-%d")}')
                print(f"{df.loc[n].to_string()}")






