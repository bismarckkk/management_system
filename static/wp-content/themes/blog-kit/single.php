<?php
/**
 * The template for displaying all single posts
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/#single-post
 *
 * @package Blog_Kit
 */

get_header();

$postid   = get_the_ID();

// Disable sidebar
$disable_sidebar_only = get_post_meta( absint( $postid ), 'disable_sidebar_only', true );
$disable_sidebar = get_post_meta( absint( $postid ), 'disable_sidebar', true );

if( ( 'checked' === $disable_sidebar_only || 'checked' === $disable_sidebar ) ){
    $main_class = 'site-main sidebar-disabled';
}else{
    $main_class = 'site-main';
}

if( ( 'checked' === $disable_sidebar_only ) ){
    $main_class .= ' background-active';
}

// Disable top and bottom space
$disable_space = get_post_meta( absint( $postid ), 'disable_space', true );
if( ( 'checked' === $disable_space ) ){
    $content_class = 'content-space-disabled';
}else{
    $content_class = 'content-space-enabled';
}

?>

	<main id="main" class="<?php echo $main_class.' '.$content_class; ?>" role="main">
		<div class="container">
			<div id="primary" class="content-area">
                <i><h3><font color="#66CCFF">本文由波斯猫原创，未经许可，严禁转载<br><br></font></h3></i>
				<?php
				while ( have_posts() ) :
					the_post();

					get_template_part( 'template-parts/content', get_post_type() );

					the_post_navigation(
						    array(
							    'next_text' => '<span class="nav-post-title nav-post-title-next">%title &rarr;</span>',
							    'prev_text' => '<span class="nav-post-title nav-post-title-previous">&larr; %title</span>',
						    )
					);

					// If comments are open or we have at least one comment, load up the comment template.
					if ( comments_open() || get_comments_number() ) :
						comments_template();
					endif;

				endwhile; // End of the loop.
				?>
                <i><h3><font color="#66CCFF"><br><br>本文由波斯猫原创，未经许可，严禁转载</font></h3></i>
			</div><!-- #primary -->

			<?php 

			if ( ( 'checked' !== $disable_sidebar_only ) && ( 'checked' !== $disable_sidebar ) ) {
			
				get_sidebar(); 

			} ?>

		</div><!-- .container -->
	</main><!-- #main -->
	
<?php
get_footer();