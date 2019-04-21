var account_info = ['first_name', 'last_name', 'username', 'gpa', 'on_campus', 'is_working'];
    function load_student_info(student_info) {
        for(var i = 0; i < account_info.length; i++) {
            var input_field = document.createElement("INPUT");
            input_field.setAttribute("type", "text");
            input_field.setAttribute("name", account_info[i]);
            input_field.setAttribute("value", student_info[i]);
            document.body.append(input_field);
            move_submit_button_to_bottom("student_info_button");
        }
    }

    var course_info = ['course_name', 'course_level', 'credit_hours', 'course_type_name', 'grade_points'];
    var j = 0;
    function load_course_info(course) {
        for(var item in course) {
            var input_field = document.createElement("INPUT");
            input_field.setAttribute("type", "text");
            input_field.setAttribute("name", course_info[j]);
            input_field.setAttribute("value", course);
            document.body.append(input_field);
            move_submit_button_to_bottom("student_info_button");
            j++;
        }
    }

    function add_course_to_form() {
        var x = 0;
        var course_form = document.getElementById("course_form");
        for(var item in course_info) {
            var input_field = document.createElement("INPUT");
            input_field.setAttribute("type", "text");
            input_field.setAttribute("value", course_info[x]);
            input_field.setAttribute("name", course_info[x]);
            course_form.appendChild(input_field);
            x++;
        }
        course_form.appendChild(document.createElement("br"));
        move_submit_button_to_bottom("course_form_button");
    }

    function move_submit_button_to_bottom(elementId) {
        var submit_button = document.getElementById(elementId);
        var parent_element = submit_button.parentElement;
        parent_element.removeChild(submit_button);
        parent_element.appendChild(submit_button);
    }