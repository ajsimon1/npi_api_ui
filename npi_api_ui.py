# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:48:47 2017

@author: adam

The NPPES has an API to ping the database based on the URL
https://npiregistry.cms.hhs.gov/api/. and an accompanying query string
This app provides a UI to search by select criteria, and format the
returned json into readable format
"""

import datetime
import json
import logging
import requests
import tkinter

# logging config
logging.basicConfig(filename='npi_api.log', level=logging.INFO)

class NPI_API():
    def __init__(self, master):
        self.master = master
        # build windows
        # main window houses whole app
        self.mainframe = tkinter.Frame(self.master, bg='white')
        self.mainframe.pack(fill=tkinter.BOTH, expand=True)
        # entry window houses entry elements and labels
        self.entryframe = tkinter.Frame(self.mainframe, bg='white')
        self.entryframe.grid(row=0, sticky='ew')
        # button windows holds submit button
        self.buttonframe = tkinter.Frame(self.mainframe, bg='white')
        self.buttonframe.grid(row=1)
        # results window holds result provided by API
        self.resultsframe = tkinter.Frame(self.mainframe, bg='white')
        self.resultsframe.grid(row=2)
        # variables
        self.TEST_TEXT = 'this is a test, for text'
        # build funcions
        self.build_grids()
        self.build_banner()
        self.build_name_fields()
        self.build_npi_facility_fields()
        self.build_buttons()
        self.build_results()

    def build_grids(self):
        self.mainframe.columnconfigure(0)
        self.mainframe.rowconfigure(0)
        self.mainframe.rowconfigure(1)
        self.mainframe.rowconfigure(2)
        self.entryframe.columnconfigure(0, weight=0)
        self.entryframe.columnconfigure(1, weight=1)
        self.entryframe.columnconfigure(2, weight=0)
        self.entryframe.columnconfigure(3, weight=1)
        self.entryframe.rowconfigure(0, weight=0)
        self.entryframe.rowconfigure(1, weight=0)
        self.entryframe.rowconfigure(2, weight=0)
        self.buttonframe.columnconfigure(0, weight=0)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=0)
        self.buttonframe.rowconfigure(0)
        self.resultsframe.columnconfigure(0, weight=1)
        self.resultsframe.rowconfigure(0)
        self.resultsframe.rowconfigure(1, weight=1)

    def build_banner(self):
        banner = tkinter.Label(
                self.entryframe,
                text='To search for NPI, add any or all of the below fields and click search',
                fg='white',
                bg='blue',
                )
        banner.grid(
                row=0, columnspan=5,
                sticky='ew')

    def build_name_fields(self):
        self.f_name_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                takefocus=True
                )
        self.f_name_lbl = tkinter.Label(
                self.entryframe,
                text='First Name:',
                bg='white'
                )
        self.f_name_entry.grid(
                row=1, column=1,
                sticky='ew',
                pady=15,
                padx=5,
                )
        self.f_name_lbl.grid(
                row=1, column=0,
                sticky='w',
                pady=15,
                padx=5,
                )
        self.l_name_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.l_name_lbl = tkinter.Label(
                self.entryframe,
                text='Last Name:',
                bg='white'
                )
        self.l_name_entry.grid(
                row=1, column=3,
                sticky='ew',
                pady=15,
                padx=5,
                )
        self.l_name_lbl.grid(
                row=1, column=2,
                sticky='w',
                pady=15,
                padx=5,
                )

    def build_npi_facility_fields(self):
        self.npi_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.npi_lbl = tkinter.Label(
                self.entryframe,
                text='NPI:',
                bg='white'
                )
        self.npi_entry.grid(
                row=2, column=1,
                sticky='ew',
                padx=5,
                )
        self.npi_lbl.grid(
                row=2, column=0,
                sticky='w',
                padx=5,
                )
        self.state_name_entry = tkinter.Entry(
                self.entryframe,
                bg='white',
                )
        self.state_name_lbl = tkinter.Label(
                self.entryframe,
                text='State:',
                bg='white'
                )
        self.state_name_entry.grid(
                row=2, column=3,
                sticky='ew',
                padx=5,
                )
        self.state_name_lbl.grid(
                row=2, column=2,
                sticky='w',
                padx=5,
                )

    def build_buttons(self):
        self.submit_btn = tkinter.Button(
                self.buttonframe,
                text='Submit',
                command=self.query_npi_api
                )
        self.submit_btn.grid(
                row=0, column=0,
                sticky='ew',
                pady=20,
                padx=20,
                )
        self.clear_btn = tkinter.Button(
                self.buttonframe,
                text='Clear',
                command=self.clear
                )
        self.clear_btn.grid(
                row=0, column=1,
                sticky='ew',
                pady=20,
                padx=20,
                )
        """
        self.export_btn = tkinter.Button(
                self.buttonframe,
                text='Export to Clipboard',
                command=self.export
                )
        self.export_btn.grid(
                row=0, column=2,
                sticky='ew',
                pady=20,
                )
        """

    def build_results(self):
        self.results_win_match_records = tkinter.Label(
                self.resultsframe,
                bg='white',
                )
        self.results_win_match_records.grid(
                row=0,
                sticky='news')
        self.results_win_data = tkinter.Entry(
                self.resultsframe,
                relief='flat',
                bg='white',
                )
        self.results_win_data.grid(
                row=1,
                sticky='news')

    # function to grab the data from API based on a query values entered in UI
    def query_npi_api(self):
        print("function triggered")
        # set url of api
        url = "https://npiregistry.cms.hhs.gov/api/"
        query_list = ["?limit=1"]
        print(query_list)
        if self.f_name_entry.get():
            final_fname_str = 'first_name='+self.f_name_entry.get()
            query_list.append(final_fname_str)
            print(query_list)
        if self.l_name_entry.get():
            final_lname_str = 'last_name='+self.l_name_entry.get()
            query_list.append(final_lname_str)
            print(query_list)
        if self.npi_entry.get():
            final_npi_str = 'npi='+self.npi_entry.get()
            query_list.append(final_npi_str)
            print(query_list)
        if self.state_name_entry.get():
            final_st_name_str = 'state='+self.state_name_entry.get()
            query_list.append(final_st_name_str)
            print(query_list)
        session = requests.session()
        final_var = str("&".join(query_list))
        print(final_var)
        response = session.get(url+final_var)
        res_json = json.loads(response.text)
        final_records_txt = 'There is/are {} matching results'.format(res_json['result_count'])
        final_dr_txt = '{} {}, {} :: '.format(res_json['results'][0]['basic']['first_name'],
                                                            res_json['results'][0]['basic']['last_name'],
                                                            res_json['results'][0]['basic']['credential'])
        final_npi_text = '{}'.format(res_json['results'][0]['number'])
        final_results_txt = final_dr_txt + '\n' + final_npi_text
        self.results_win_match_records.config(text=final_records_txt)
        self.results_win_data.insert(0, final_results_txt)
        self.results_win_data.config(state='readonly', readonlybackground='white')


    def clear(self):
        self.results_win_match_records.config(text='')
        self.results_win_data.config(state=tkinter.NORMAL)
        self.results_win_data.delete(0, tkinter.END)
        
    

if __name__ == '__main__':
    main_window = tkinter.Tk()
    main_window.title('P4 - NPI Registry Search')
    main_window.geometry('650x350')
    app = NPI_API(main_window)
    logging.info('NPI app opened at {}'.format(datetime.datetime.now()))
    main_window.mainloop()
