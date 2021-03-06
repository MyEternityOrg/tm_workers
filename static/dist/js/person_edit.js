const f_time = document.getElementById('id_f_time');
const t_time = document.getElementById('id_t_time');
const f_main = document.getElementById('f_main');
const f_delete = document.getElementById('f_delete');
const p_name = document.getElementById('id_person_name');
const p_city = document.getElementById('id_p_city');
const p_birthday = document.getElementById('id_p_birthday');
const max_hour = document.getElementById('js_validate').getAttribute('hour');
const staff = document.getElementById('js_validate').getAttribute('staff');
const max_interval_hours = document.getElementById('js_validate').getAttribute('max_hours');

$(function () {
    $('#f_time_picker').datetimepicker({
        pickDate: false,
        pickSeconds: false
    });
});

$(function () {
    $('#t_time_picker').datetimepicker({
        pickDate: false,
        pickSeconds: false
    });
});

$(function () {
    $('#p_birthday_picker').datetimepicker({
        language: 'ru',
        pickTime: false,
        format: 'yyyy-MM-dd'
    });
});

try {
    document.addEventListener('DOMContentLoaded', function (event) {
        if (f_time.value.length < 3) {
            f_time.value = '09:00'
        }
        ;
        if (t_time.value.length < 3) {
            t_time.value = '17:00'
        }
        ;
        if (p_birthday.value.length < 5) {
            p_birthday.value = '2000-01-01'
        } else {
            if (p_birthday.value.includes(".")) {
                let ar
                ar = p_birthday.value.split(".")
                p_birthday.value = ar[ar.length - 1] + '-' + ar[ar.length - 2] + '-' + ar[ar.length - 3]
            }
        }
        let ar_ft = f_time.value.split(":")
        f_time.value = ar_ft[0] + ':' + ar_ft[1]
        let ar_tt = t_time.value.split(":")
        t_time.value = ar_tt[0] + ':' + ar_tt[1]
    });
} catch (e) {
}


function test_fio(value) {
    let regExp = /^([А-ЯA-Z]|[А-ЯA-Z][\x27а-яa-z]{1,}|[А-ЯA-Z][\x27а-яa-z]{1,}\-([А-ЯA-Z][\x27а-яa-z]{1,}|(оглы)|(кызы)))\040[А-ЯA-Z][\x27а-яa-z]{1,}(\040[А-ЯA-Z][\x27а-яa-z]{1,})?$/
    return regExp.test(value)
}

function get_current_age(_date) {
    let date = new Date(_date)
    let now = new Date();
    let current_year = now.getFullYear();
    let year_diff = current_year - date.getFullYear();
    let birthday_this_year = new Date(current_year, date.getMonth(), date.getDate());
    let has_had_birthday_this_year = (now >= birthday_this_year);
    return has_had_birthday_this_year
        ? year_diff
        : year_diff - 1;
}


try {
    f_delete.addEventListener('submit', function (e) {
        let current_hour = new Date().getHours()
        if (!staff) {
            if (current_hour >= max_hour) {
                result.innerHTML = '<p><div class="alert alert-danger" role="alert">Данную запись нельзя удалить после ' + max_hour + ':00 текущего дня!</div></p>'
                e.preventDefault()
            } else {
            }
        }
    });
} catch (e) {
}

try {
    f_main.addEventListener('submit', function (e) {
        let max_interval = max_interval_hours * 60 * 60 * 1000
        let fd = new Date()
        let td = new Date()
        let current_hour = new Date().getHours()
        fd.setHours.apply(fd, f_time.value.split(":"));
        td.setHours.apply(td, t_time.value.split(":"));
        let interval = td - fd

        if (fd >= td) {
            result.innerHTML = '<p><div class="alert alert-danger" role="alert">Введен некоррекнтый интервал! Проверьте что время начала работы не больше времени завершения!</div></p>'
            e.preventDefault();
        } else if (interval > max_interval) {
            result.innerHTML = '<p><div class="alert alert-danger" role="alert">Подолжительность рабочего дня не может превышать '+ max_interval_hours +' часов!</div></p>'
            e.preventDefault();
        }
        if (!test_fio(p_name.value)) {
            result.innerHTML = '<p><div class="alert alert-danger" role="alert">Для сотрудника введены некорректные данные. <br>Требуется: <b>Фамилия Имя</b> или <b>Фамилия Имя Отчество</b>.</div></p>'
            e.preventDefault();
        }
        if (!staff) {
            if (current_hour >= max_hour) {
                result.innerHTML = '<p><div class="alert alert-danger" role="alert">Данные нельзя редактировать/создавать после ' + max_hour + ':00 текущего дня!</div></p>'
                e.preventDefault()
            }
        }
        let age = get_current_age(p_birthday.value)
        if (age >= 18) {
        } else {
            result.innerHTML = '<p><div class="alert alert-danger" role="alert">Сотрудник слишком молодой. В РФ запрещено использовать детский труд.</div></p>'
            e.preventDefault();
        }
    });
} catch (e) {
}
