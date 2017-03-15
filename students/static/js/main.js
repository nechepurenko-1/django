function initJournal() {
    var indicator = $('#ajax-progress-indicator');
    $('.day-box input[type="checkbox"]').click(function (event) {
    var box = $(this);
    $.ajax(box.data('url'),{
        'type':'POST',
        'async':true,
        'dataType':'json',
        'data':{
            'pk': box.data('student-id'),
            'date': box.data('date'),
            'present': box.is(':checked') ? '1' : "" ,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        'beforeSend':function (xhr, settings) {
            indicator.show()
        },
        'error':function (xhr, status, error) {
             //allert(error);
             $(".alert-warning").addClass("alert-danger").html(error);
            indicator.hide();
        },
        'success': function (data, status, xhr) {
            indicator.hide();
        }
        });
       });
    }

function initGroupSelector() {
    $('#group-selector select').change(function (event) {
        var group = $(this).val();

        if (group) {
            $.cookie('current_group', group, {'path': '/', 'expires': 365});
        }
        else{
            $.removeCookie('current_group', {'path': '/'});
        }
        location.reload(true);

        return true;
    });
}

function initDateFields(){
    $('input.dateinput').datetimepicker({
        'format': 'YYYY-MM-DD',
        locale: 'uk'
    }).on('dp.hide', function(event){
    $(this).blur();
    });
}

function initDateTimeFields(){
    $('input.datetimeinput').datetimepicker({
        'format': 'YYYY-MM-DD HH:mm:ss',
        locale: 'uk'
    }).on('dp.hide', function(event){
    $(this).blur();
    });
}

    $(document).ready(function () {
    initJournal();
    initGroupSelector();
    initDateFields();
    initDateTimeFields();
});