<?php
/**
 * Template part for displaying posts
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
	if( is_singular() ){ 

		if ( ( 'checked' !== $disable_title ) ) { ?>

			<header class="entry-header">
				<?php
					
				the_title( '<h1 class="entry-title">', '</h1>' );
				
				if ( 'post' === get_post_type() ) { ?>
					
					<div class="entry-meta">
						<?php
						blog_kit_posted_on();
						blog_kit_posted_by();
						?>
					</div><!-- .entry-meta -->
					
					<?php 
				} ?>
			</header><!-- .entry-header -->
			<?php
		}

	}else{ ?>

		<header class="entry-header">
			<?php
			if ( is_singular() ) :
				the_title( '<h1 class="entry-title">', '</h1>' );
			else :
				the_title( '<h2 class="entry-title"><a href="' . esc_url( get_permalink() ) . '" rel="bookmark">', '</a></h2>' );
			endif;

			if ( 'post' === get_post_type() ) :
				?>
				<div class="entry-meta">
					<?php
					blog_kit_posted_on();
					blog_kit_posted_by();
					?>
				</div><!-- .entry-meta -->
			<?php endif; ?>
		</header><!-- .entry-header -->
		<?php
	} ?>

	<?php 
	if( is_singular() ){
		if( ( 'checked' !== $disable_feat_image ) ){
			blog_kit_post_thumbnail(); 	
		} 
	}else{
		blog_kit_post_thumbnail();
	} ?>

	<div class="entry-content">
		<?php
		if ( is_singular() ) :
			the_content( sprintf(
				wp_kses(
					/* translators: %s: Name of current post. Only visible to screen readers */
					__( 'Continue reading<span class="screen-reader-text"> "%s"</span>', 'blog-kit' ),
					array(
						'span' => array(
							'class' => array(),
						),
					)
				),
				get_the_title()
			) );

			wp_link_pages( array(
				'before' => '<div class="page-links">' . esc_html__( 'Pages:', 'blog-kit' ),
				'after'  => '</div>',
			) );
		else :
			the_excerpt();
		endif;
		?>
	</div><!-- .entry-content -->

	<?php if ( is_singular() ) : ?>
		<footer class="entry-footer">
			<?php blog_kit_entry_footer(); ?>
		</footer><!-- .entry-footer -->
	<?php endif; ?>
	
</article><!-- #post-<?php the_ID(); ?> -->
