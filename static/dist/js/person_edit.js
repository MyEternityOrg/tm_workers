const f_time = document.getElementById('id_f_time');
const t_time = document.getElementById('id_t_time');
const f_main = document.getElementById('f_main')

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


document.addEventListener('submit', function (e) {
	let fd = new Date()
	let td = new Date()
	fd.setHours.apply(fd, f_time.value.split(":"));
	td.setHours.apply(td, t_time.value.split(":"));
	if (fd >= td) {
		result.innerHTML = '<p><div class="alert alert-danger" role="alert">Введен некоррекнтый интервал! Проверьте что время начала работы не больше времени завершения!</div></p>'
		e.preventDefault();
	}
});
