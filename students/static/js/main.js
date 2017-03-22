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

function initEditStudentPage(){
    $('a.student-edit-form-link').click(function(event){
    var link = $(this);
    $.ajax({
        'url': link.attr('href'),
        'dataType': 'html',
        'type': 'get',
        'success': function(data,status,xhr){
            if (status != 'success'){
                alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
                return false;
            }
            var modal = $('#myModal');
            html = $(data), form = html.find('#content-column form');
        modal.find('.modal-title').html(html.find('#content-column h2').text());
        modal.find('.modal-body').html(form);
        initEditStudentForm(form,modal);
        modal.modal({
            'keyboard': false,
            'backdrop' : false,
            'show': true
            });
            },
        'error': function(){
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
        return false;
        },
        'beforeSend': function() {
                $('.ajax-loader').show();
            },
        'complete': function() {
                $('.ajax-loader').hide();
            }
    });
    return false;
    });
}

function initEditStudentForm(form,modal){
    initDateFields();
    initPhotoField();
    form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
    });
    form.ajaxForm({
    'dataType': 'html',
    'error': function(){
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
        return false;
    },
    'success': function(data,status,xhr){
    var html = $(data), newform = html.find('#content-column form');
    modal.find('.modal-body').html(html.find('.alert'));
    if (newform.lenght > 0 ){
        modal.find('.modal-body').append(newform);
        initEditStudentForm(newform, modal);
    } else {
        setTimeout(function(){location.reload(true);}, 500);
        }
    },
    'beforeSend': function() {
            $('.ajax-loader-modal img').show();
            $('input, select, textarea, a, button').attr('disabled', 'disabled');
        },
        'complete': function() {
            $('.ajax-loader-modal img').hide();
            $('input, select, textarea, a, button').removeAttr('disabled', 'disabled');
        }
    });

}

function initAddStudentPage(){
    $('a.student-add-form-link').click(function(event){
    var link = $(this);
    $.ajax({
        'url': link.attr('href'),
        'dataType': 'html',
        'type': 'get',
        'success': function(data,status,xhr){
            if (status != 'success'){
                alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
                return false;
            }
            var modal = $('#myModal');
            html = $(data), form = html.find('#content-column form');
        modal.find('.modal-title').html(html.find('#content-column h2').text());
        modal.find('.modal-body').html(form);
        initAddStudentForm(form,modal);
        modal.modal({
            'keyboard': false,
            'backdrop' : false,
            'show': true
            });
            },
        'error': function(){
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
        return false;
        },
        'beforeSend': function() {
                $('.ajax-loader').show();
            },
        'complete': function() {
                $('.ajax-loader').hide();
            }
    });
    return false;
    });
}

function initAddStudentForm(form,modal){
    initDateFields();
    initPhotoField();
    form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
    });
    form.ajaxForm({
    'dataType': 'html',
    'error': function(){
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
        return false;
    },
    'success': function(data,status,xhr){
    var html = $(data), newform = html.find('#content-column form');
    modal.find('.modal-body').html(html.find('.alert'));
    if (newform.lenght > 0 ){
        modal.find('.modal-body').append(newform);
        initEditStudentForm(newform, modal);
    } else {
        setTimeout(function(){location.reload(true);}, 500);
        }
    },
    'beforeSend': function() {
            $('.ajax-loader-modal img').show();
            $('input, select, textarea, a, button').attr('disabled', 'disabled');
        },
        'complete': function() {
            $('.ajax-loader-modal img').hide();
            $('input, select, textarea, a, button').removeAttr('disabled', 'disabled');
        }
    });

}

function navTabs() {
    var navLinks = $('.nav-tabs li > a');
    navLinks.click(function(event) {
        var url = this.href;
        $.ajax({
            'url': url,
            'dataType': 'html',
            'type': 'get',
            'success': function(data, status, xhr){
                // check if we got successful responcse
                if (status != 'success') {
                    alert("There was an error on the server. Please, try again a bit later.");
                    return false;
                };

                // update table
                var content = $(data).find('#content-columns');
                var pageTitle = content.find('h2').text();
                $(document).find('#content-columns').html(content.html());
                navLinks.each(function(index){
                    if (this.href === url) {
                      $(this).parent().addClass('active');
                    } else {
                      $(this).parent().removeClass('active');
                    };
                });
                // update uri in address bar
                window.history.pushState("string", pageTitle, url);
                // update page title
                document.title = $(data).filter('title').text();
            },
            'error': function() {
                alert("There was an error on the server. Please, try again a bit later.");
                return false;
            },
            'beforeSend': function() {
                $('.ajax-loader').show();
            },
            'complete': function() {
                $('.ajax-loader').hide();
                initFunctions();
            }
        });
        event.preventDefault();
    });
}

function initPhotoField(){
    var imgUrl = $('#div_id_photo a').attr('href');
    var imgHtml = '<img heigh="30" width="30" class=img-circle src=' +  imgUrl + '/>'
    $('#div_id_photo a').html(imgHtml);
}


$(document).ready(function(){
    initFunctions();
    navTabs();
    initGroupSelector();
});
function initFunctions(){
    initJournal();
    initDateFields();
    initDateTimeFields();
    initEditStudentPage();
    initAddStudentPage()

}