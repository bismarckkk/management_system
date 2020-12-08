<?php
/**
 * The template for displaying the footer
 *
 * Contains the closing of the #content div and all content after.
 *
 * @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package Blog_Kit
 */

?>

	</div><!-- #content -->

	<?php

	if ( is_active_sidebar( 'footer-1' ) ||
		 is_active_sidebar( 'footer-2' ) ||
		 is_active_sidebar( 'footer-3' ) ||
		 is_active_sidebar( 'footer-4' ) ) :
	?>

		<aside id="footer-widgets" class="widget-area site-footer" role="complementary">
			<div class="container">
				<?php
				$column_count = 0;

				for ( $i = 1; $i <= 4; $i++ ) {

					if ( is_active_sidebar( 'footer-' . $i ) ) {
						$column_count++;
					}

				} ?>

				<div class="inner-wrapper">
					<?php

					$column_class = 'footer-widgets-column  footer-column-' . absint( $column_count );

					for ( $i = 1; $i <= 4 ; $i++ ) {

						if ( is_active_sidebar( 'footer-' . $i ) ) { ?>

							<div class="<?php echo esc_attr( $column_class ); ?>">

								<?php dynamic_sidebar( 'footer-' . $i ); ?>

							</div>

							<?php
						}

					} ?>
				</div><!-- .inner-wrapper -->
			</div><!-- .container -->
		</aside><!-- #footer-widgets -->

	<?php endif; ?>

	<footer id="colophon" class="bottom-info" role="contentinfo">
		<div class="container">
			<div class="copyrights-info">
				<?php 

				$copyright_text = blog_kit_get_option('copyright_text');

				if ( ! empty( $copyright_text ) ) : ?>

					<div class="copyright">

						<?php echo wp_kses_data( $copyright_text ); ?>

					</div><!-- .copyright -->

					<?php 

				endif; 
                
                ?>
                <br>ICP证:
                <a href="https://www.beian.miit.gov.cn">鄂ICP备20003159号-1</a>

				<div class="site-info">
				    <?php printf( "powered by 波斯猫" ); ?>
				</div><!-- .site-info -->
			</div>
		</div><!-- .container -->
	</footer><!-- #colophon -->

<script type="text/javascript">
document.addEventListener('visibilitychange',function(){if(document.visibilityState=='hidden'){normal_title=document.title;document.title='性感荷官在线发牌';}else{document.title=normal_title;}});
 </script>

</div><!-- #page -->

<script type="text/javascript">
/*富强民主文明和谐*/
var a_idx = 0;
jQuery(document).ready(function($) {
$("body").click(function(e) {
var a = new Array("富强", "民主", "文明", "和谐", "自由", "平等", "公正" ,"法治", "爱国", "敬业", "诚信", "友善");
var $i = $("<span/>").text(a[a_idx]);
a_idx = (a_idx + 1) % a.length;
var x = e.pageX,
y = e.pageY;
$i.css({
"z-index": 9999,
"top": y - 15,
"left": x - 20,
"position": "absolute",
"font-weight": "bold",
"color": "#66ccff"
});
$("body").append($i);
$i.animate({
"top": y - 180,
"opacity": 0
},
1500,
function() {
$i.remove();
});
});
});
</script>
<?php wp_footer(); ?>

<div id="landlord" style="display: block;">
    <div class="message" style="opacity:0"></div>
    <canvas id="live2d" width="280" height="250" class="live2d"></canvas>
</div>


<script type="text/javascript">
    var message_Path = '/live2d/'
    var home_Path = 'http://101.37.89.101/'  //此处修改为你的域名，必须带斜杠
</script>
</script>

<script type="text/javascript" charset="utf-8" src="custom/yinghua.js"></script>
<script type="text/javascript">  
function browserRedirect() {  
var sUserAgent = navigator.userAgent.toLowerCase();  
var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";  
var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";  
var bIsMidp = sUserAgent.match(/midp/i) == "midp";  
var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";  
var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";  
var bIsAndroid = sUserAgent.match(/android/i) == "android";  
var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";  
var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";  
// 浏览设备为  
if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) { 
//手机浏览 
document.getElementById("closesukura").value = "开启樱花";
} else {  
  
//PC浏览
	document.write('<script type="text/javascript" charset="utf-8" src="live2d/js/message.js"><\/script>');  
	document.write('<script type="text/javascript" charset="utf-8" src="live2d/js/live2d.js"><\/script>');  
	stopp();
}  
}  
browserRedirect();  
</script> 
<script type="text/javascript">
    loadlive2d("live2d", "/live2d/model/tia/model.json");
</script>
</body>

<script type="text/javascript">
	function l2dswitch()
	{
		if(getComputedStyle(document.getElementById('landlord'),null).getPropertyValue('display') == "block")
			{
				jQuery('#landlord').css('display', 'none')
				document.getElementById("lswitch").value = "开启L2D";
			}
		else
		{
			jQuery('#landlord').css('display', 'block')
			loadlive2d("live2d", "/live2d/model/tia/model.json");
			document.getElementById("lswitch").value = "隐藏L2D";
		}
	}
</script>

<script type="text/javascript">
	jQuery.getJSON('https://v1.hitokoto.cn/', {"c":"a"}, function(result){
        console.info("type = " + result.type);
		var tpp = result.hitokoto + '<br>——' + result.from;
		document.getElementById('tbox').innerHTML = tpp;
  	});
	var t2 = window.setInterval(function() {
		jQuery("#tbox").fadeOut("1000");
		var t1 = window.setTimeout(function() {
			jQuery.getJSON('https://v1.hitokoto.cn/', {"c":"a"}, function(result){
                console.info("type = " + result.type);
				var tpp = result.hitokoto + '<br>——' + result.from;
				document.getElementById('tbox').innerHTML = tpp;
			});
			jQuery("#tbox").delay("60").fadeIn("1000");
		},900);
	},20000);
</script>
</html>