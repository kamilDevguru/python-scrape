from selenium import webdriver
import csv

driver = webdriver.Chrome('./chromedriver')
driver.get("https://apps.health.tn.gov/FacilityListings/")
search_keywords = ['Assisted Care Living Facility',
                   'Adult Care Home', 'Home for the Aged']

with open('result.csv', mode='w') as result:
    # Open csv file and write header
    csv_writer = csv.writer(result, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([
        'Community Name',
        'Street Address',
        'City',
        'State',
        'Zip',
        'Phone',
        'Administrator',
        'Owner Company',
        'Owner Street Address',
        'Owner City',
        'Owner State',
        'Owner Zip',
        'Owner Phone',
        'Facility License Number',
        'Status',
        'Number of Beds',
        'Date of Last Survey',
        'Date of Original Licensure',
        'Date of Expiration',
        'Disciplinary Actions'
    ])

    for keyword in search_keywords:
        print('*********************************')
        print('Keyword: %s' % keyword)
        # Select select box for items
        try:
            search_box = driver.find_element_by_id(
                'CurrentSearchModel_FacilityType')
            search_box.click()
        except:
            print('Network error')
            driver.close()

        # Select target item from select box
        options = driver.find_elements_by_tag_name('option')

        target_option = next(item for item in options if item.text == keyword)
        target_option.click()

        # Click search button
        search_btn = driver.find_element_by_xpath(
            '//*[@id="MainContent"]/div/form[1]/div/div[5]/input')
        search_btn.click()

        # Find table
        table = driver.find_element_by_xpath(
            '//*[@id="MainContent"]/table/tbody')
        records = table.find_elements_by_tag_name('tr')
        print(len(records))
        for record in records:
            new_row = {
                'community_name': '',
                'street_address': '',
                'city': '',
                'state': '',
                'zip': '',
                'phone': '',
                'administrator': '',
                'owner_company': '',
                'owner_street_address': '',
                'owner_city': '',
                'owner_state': '',
                'owner_zip': '',
                'owner_phone': '',
                'facility_license_number': '',
                'status': '',
                'number_of_beds': '',
                'date_of_last_survey': '',
                'date_of_original_licensure': '',
                'date_of_expiration': '',
                'disciplinary_actions': ''
            }
            first_item = record.find_elements_by_tag_name('td')[1]
            second_item = record.find_elements_by_tag_name('td')[2]
            third_item = record.find_elements_by_tag_name('td')[3]

            # Extract data from table row
            # first cell
            first_info_list = [str(s) for s in first_item.text.splitlines()]
            new_row['community_name'] = first_info_list[0]
            new_row['street_address'] = first_info_list[1]
            try:
                new_row['city'] = first_info_list[2].split()[0].split(',')[0]
                new_row['state'] = first_info_list[2].split()[1]
                new_row['zip'] = first_info_list[2].split()[2]
            except:
                new_row['city'] = ''
                new_row['state'] = ''
                new_row['zip'] = ''

            try:
                new_row['administrator'] = first_info_list[3].split(':')[
                    1].strip()
            except:
                new_row['administrator'] = ''
            new_row['phone'] = first_info_list[4]

            # second cell
            second_info_list = [str(s) for s in second_item.text.splitlines()]
            try:
                new_row['owner_company'] = second_info_list[2]
                new_row['owner_street_address'] = second_info_list[3]
                new_row['owner_city'] = second_info_list[4].split()[
                    0].split(',')[0]
                new_row['owner_state'] = second_info_list[4].split()[
                    1]
                new_row['owner_zip'] = second_info_list[4].split()[2]
                new_row['owner_phone'] = second_info_list[5]
            except:
                new_row['owner_company'] = ''
                new_row['owner_street_address'] = ''
                new_row['owner_city'] = ''
                new_row['owner_state'] = ''
                new_row['owner_zip'] = ''
                new_row['owner_phone'] = ''

            # third cell
            third_info_list = [str(s) for s in third_item.text.splitlines()]
            try:
                new_row['facility_license_number'] = third_info_list[0].split(':')[
                    1].strip()
                new_row['status'] = third_info_list[1].split(':')[1].strip()
                new_row['number_of_beds'] = third_info_list[2].split(':')[
                    1].strip()
                new_row['date_of_last_survey'] = third_info_list[3].split(':')[
                    1].strip()
                new_row['date_of_original_licensure'] = third_info_list[4].split(':')[
                    1].strip()
                new_row['date_of_expiration'] = third_info_list[5].split(':')[
                    1].strip()
                new_row['disciplinary_actions'] = third_info_list[len(
                    third_info_list) - 1]
            except:
                new_row['facility_license_number'] = ''
                new_row['status'] = ''
                new_row['number_of_beds'] = ''
                new_row['date_of_last_survey'] = ''
                new_row['date_of_original_licensure'] = ''
                new_row['date_of_expiration'] = ''
                new_row['disciplinary_actions'] = ''

            csv_writer.writerow([item[1] for item in new_row.items()])

        return_button = driver.find_element_by_xpath(
            '//*[@id="MainContent"]/div[1]/div[2]/a')
        return_button.click()

driver.close()