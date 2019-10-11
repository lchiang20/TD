            $(document).on("click", '#login', function(e) {
                $(document).ready(function() {
                    var data = {
                        'email': 'filter_city',
                        'id_A': "FGDKJ"
                    };
                    $.ajax({
                        url: '/login_request/',
                        data: data,
                        type: 'GET',
                        success: function(response) { // Go through appliction if does ork then prints
                            console.log(response);
                        },
                        error: function(error) {
                            console.log(error);
                        }
                    });
                });
            })

            $(document).ready(function() {
                var data = {
                    'email': 'filter_city',
                    'id_A': "FGDKJ",
                };
                $.ajax({
                    url: '/login_request/',
                    data: data,
                    type: 'GET',
                    success: function(response) { // Go through appliction if does ork then prints
                        console.log(response);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            });