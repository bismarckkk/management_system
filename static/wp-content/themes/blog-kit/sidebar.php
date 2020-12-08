<?php
/**
 * The sidebar containing the main widget area
 *
 * @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package Blog_Kit
 */

if ( ! is_active_sidebar( 'sidebar-1' ) ) {
	return;
}
?>

<aside id="secondary" class="widget-area">
	<div class="side-bar">
		<section id="eswitch">
			<div id="espc" display="block">
				<h2 class="widget-title">
					特效开关<br>
				</h2>
				<p>
					注：L2D功能在手机上无法正常使用<br>樱花功能已经完成手机适配<br>因其可能导致卡顿默认关闭
				</p>
				<div style="text-align:center">
					<input type="button" name="closesukura" id ="closesukura" value="关闭樱花" onclick="stopp();"/>
				<input type="button" name="lswitch" id ="lswitch" value="隐藏L2D" onclick="l2dswitch();"/>
				</div>
			</div>
		</section>
		<?php dynamic_sidebar( 'sidebar-1' ); ?>
	</div>
</aside><!-- #secondary -->
