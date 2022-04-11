MESSAGES = {'sucess_account': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                               'message': 'Account created successfully.'},
            'sucess_login': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                             'message': 'Login successful.'},
            'error_email': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger',
                            'message': 'E-mail already registered'},
            'invalid_email': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Invalid Email !'},
            'error_password': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Wrong password!'},
            'activity_added': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                               'message': 'Activity Successfully Added!'}
            }


def create_labels(mt, abl, ftl, stl, rm, fini, miss, total, nsm):
    return {'main_title': mt,
            'add_btn_label': abl,
            'first_tab_label': ftl,
            'second_tab_label': stl,
            'remaining_label': rm,
            'finished_label': fini,
            'missed_label': miss,
            'total_label': total,
            'new_session_message': nsm
            }


ACTIVITIES_DASH = {
    'gym': create_labels('GYM', 'Book New Workout', 'Next Workouts', ' Workouts History', 'Remaining Trainings',
                         'Finished Trainings', 'Missed Trainings', 'Total Time in Gym', 'Pump those numbers up! Check out this week\'s availability'),
    'parking': create_labels('Parking Garage', 'New Stall Reservation', 'Next Reservations', 'Parking History',
                             'Remaining Reservations',
                             'Finished Reservations', 'Missed Reservations', 'Total Time in Parking',
                             'Pump those numbers up! Check out this week\'s availability'),
    'tennis': create_labels('Tennis Court', 'Book New Tennis', 'Next Tennis', 'Tennis History', 'Remaining Tennis',
                            'Finished Tennis', 'Missed Tennis', 'Total Time in Tennis',
                            'Pump those numbers up! Check out this week\'s availability'),
    'party': create_labels('Party Room', 'Book New Party', 'Next Parties', 'Party History', 'Remaining Parties',
                           'Finished Parties', 'Missed Parties', 'Total Time in Party',
                           'Pump those numbers up! Check out this week\'s availability'),
    'visitors': create_labels('Visitors', 'New Visitor', 'Next Visitors', 'Visitors History', 'Remaining Visitors',
                              'Finished Visitors', 'Missed Visitors', 'Total Time in Visitors',
                              'Pump those numbers up! Check out this week\'s availability')
    }
ACTIVITY_OPTIONS = [{'name': 'gym', 'icon': 'fitness_center', 'color': '#FFC107'},
                    {'name': 'parking', 'icon': 'garage', 'color': '#FFC107'},
                    {'name': 'tennis', 'icon': 'sports_tennis', 'color': '#FFC107'},
                    {'name': 'party', 'icon': 'celebration', 'color': '#FFC107'},
                    {'name': 'visitors', 'icon': 'groups', 'color': '#FFC107'}]
                    # ,{'name': 'generate_codes', 'icon': 'manage_accounts', 'color': '#FFC107'}]
