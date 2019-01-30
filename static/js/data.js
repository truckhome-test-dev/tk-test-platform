$(document).ready(function () {

	function anchorClick(link) {
		var linkSplit = link.split('/').pop();
		$.get('/Users/asus/Desktop/Backstage/' + linkSplit, function (data) {
			console.log(data)
			$('#content').html(data);
		});

	}

	$('#nav_con li').on('click', 'a', function (e) {
		window.history.pushState(null, null, $(this).attr('href'));
		anchorClick($(this).attr('href'));
		e.preventDefault();
	});

	window.addEventListener('popstate', function (e) {
		anchorClick(location.pathname);
	});

	// 标题 导航
	var text = $('#nav_con li').eq(0).children(".nav").text();
	$('.top-nav').html(text)
	$('#nav_con li').on('click', function () {
		$(this).addClass('active').siblings().removeClass('active');
		var name = $(this).children(".nav").text()
		$('.top-nav').html(name)
	})
});