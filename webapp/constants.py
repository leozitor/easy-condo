MESSAGES = {'account_creation_success': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                               'message': 'Account created successfully.'},
            'sucess_login': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                             'message': 'Login successful.'},
            'error_email': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger',
                            'message': 'E-mail already registered'},
            'invalid_email': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Invalid Email !'},
            'error_password': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Wrong password!'},
            'activity_added': {'icon': 'bi bi-check-circle-fill', 'type': 'alert-success',
                               'message': 'Activity Successfully Added!'},
            'wrong_code': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Inserted Wrong Invitation Code! Try again'},
            'form_invalid': {'icon': 'bi bi-bookmark-x-fill', 'type': 'alert-danger', 'message': 'Informations filled incorrectly! sign up again'}
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
                             'Finished Reservations', 'Missed Reservations', 'Total Reservations in Parking',
                             'To reserve ! Check out this week\'s availability'),
    'tennis': create_labels('Tennis Court', 'New tennis Reservation', 'Next Tennis Reservations', 'Tennis History', 'Remaining Reservations',
                            'Finished Tennis', 'Missed Tennis', 'Total Reservations in Tennis',
                            'Want to play tennis! Check out this week\'s availability'),
    'party': create_labels('Party Room', 'New Reservation', 'Next Reservations', 'Party Room History', 'Remaining Reservations',
                           'Finished Reservations', 'Missed Reservations', 'Total Reservations in Party',
                           'Want to Reserve the Party Room? Check out this week\'s availability'),
    'visitors': create_labels('Visitors', 'New Visitor', 'Next Visitors', 'Visitors History', 'Remaining Visitors',
                              'Finished Visitors', 'Missed Visitors', 'Total Time in Visitors',
                              'Pump those numbers up! Check out this week\'s availability')
    }
ACTIVITY_OPTIONS = [{'name': 'gym', 'icon': 'fitness_center', 'color': '#FFC107'},
                    {'name': 'parking', 'icon': 'garage', 'color': '#FFC107'},
                    {'name': 'tennis', 'icon': 'sports_tennis', 'color': '#FFC107'},
                    {'name': 'party', 'icon': 'celebration', 'color': '#FFC107'}]
                    # {'name': 'visitors', 'icon': 'groups', 'color': '#FFC107'}]
                    # ,{'name': 'generate_codes', 'icon': 'manage_accounts', 'color': '#FFC107'}]
