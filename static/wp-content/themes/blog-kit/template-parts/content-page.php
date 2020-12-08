<?php
/**
 * Template part for displaying page content in page.php
 *
 * @link https://developer.wordpress.org/themes/basics/template-hierarchy/
 *
 * @package Blog_Kit
 */

$postid   = get_the_ID();

$disable_title 		= get_post_meta( absint($postid), 'disable_title', true );
$disable_feat_image = get_post_meta( absint($postid), 'disable_feat_image', true );
?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<?php 
	if( ( 'checked' !== $disable_title ) ){ ?>
		<header class="entry-header">
			<?php the_title( '<h1 class="entry-title">', '</h1>' ); ?>
		</header><!-- .entry-header -->
		<?php
	} ?>

	<?php 
	if( ( 'checked' !== $disable_feat_image ) ){
		blog_kit_post_thumbnail(); 	
	} ?>

	<div class="entry-content">
		<?php
		the_content();

		wp_link_pages( array(
			'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'blog-kit' ),
			'after'  => '</div>',
		) );
		?>
	</div><!-- .entry-content -->

	<?php if ( get_edit_post_link() ) : ?>
		<footer class="entry-footer">
			<?php
			edit_post_link(
				sprintf(
					wp_kses(
						/* translators: %s: Name of current post. Only visible to screen readers */
						__( 'Edit <span class="screen-reader-text">%s</span>', 'blog-kit' ),
						array(
							'span' => array(
								'class' => array(),
							),
						)
					),
					get_the_title()
				),
				'<span class="edit-link">',
				'</span>'
			);
			?>
		</footer><!-- .entry-footer -->
	<?php endif; ?>
</article><!-- #post-<?php the_ID(); ?> -->
