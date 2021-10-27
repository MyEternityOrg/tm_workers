const f_time = document.getElementById('id_f_time');
const t_time = document.getElementById('id_t_time');
const f_main = document.getElementById('f_main');
const f_delete = document.getElementById('f_main');
const p_name = document.getElementById('id_person_name');

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

document.addEventListener('DOMContentLoaded', function (event) {
	f_time.value = '09:00';
	t_time.value = '17:00';
});

function test_fio(value) {
	let regExp = /^([А-ЯA-Z]|[А-ЯA-Z][\x27а-яa-z]{1,}|[А-ЯA-Z][\x27а-яa-z]{1,}\-([А-ЯA-Z][\x27а-яa-z]{1,}|(оглы)|(кызы)))\040[А-ЯA-Z][\x27а-яa-z]{1,}(\040[А-ЯA-Z][\x27а-яa-z]{1,})?$/
	return regExp.test(value)
}

f_main.addEventListener('submit', function (e) {
	let fd = new Date()
	let td = new Date()
	fd.setHours.apply(fd, f_time.value.split(":"));
	td.setHours.apply(td, t_time.value.split(":"));
	if (fd >= td) {
		result.innerHTML = '<p><div class="alert alert-danger" role="alert">Введен некоррекнтый интервал! Проверьте что время начала работы не больше времени завершения!</div></p>'
		e.preventDefault();
	}
	if (!test_fio(p_name.value)) {
		result.innerHTML = '<p><div class="alert alert-danger" role="alert">Для сотрудника введены некорректные данные. <br>Требуется: <b>Фамилия Имя</b> или <b>Фамилия Имя Отчество</b>.</div></p>'
		e.preventDefault();
	}
});
