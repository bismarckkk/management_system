<?php
/**
 * The header for our theme
 *
 * This is the template that displays all of the <head> section and everything up until <div id="content">
 *
 * @link https://developer.wordpress.org/themes/basics/template-files/#template-partials
 *
 * @package Blog_Kit
 */

?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="profile" href="https://gmpg.org/xfn/11">
	<link rel="stylesheet" href="/live2d/css/live2d.css" />
	<?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>

<?php wp_body_open(); ?>

<div id="page" class="site">
	<header id="masthead" class="site-header">
		<div class="bottom-header">
			<div class="container">
				<div class="inner-header-wrap">
					<div class="site-branding">

						<?php 

						$site_identity = blog_kit_get_option( 'site_identity' );

						if( 'logo-only' == $site_identity ){  

							the_custom_logo(); 

						}elseif( 'title-only' == $site_identity ){

							if ( is_front_page() ) : ?>
								<h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></h1>
							<?php else : ?>
								<p class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></p>
							<?php endif;

						} else{

							if ( is_front_page() ) : ?>
								<h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></h1>
							<?php else : ?>
								<p class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></p>
							<?php endif; ?>

							<?php
							$blog_kit_description = get_bloginfo( 'description', 'display' );

							if ( $blog_kit_description || is_customize_preview() ) :
								?>
								<p class="site-description"><?php echo $blog_kit_description; /* WPCS: xss ok. */ ?></p>
							<?php endif; 
							
						} ?>

					</div><!-- .site-branding -->

					<?php 

					$show_social_icons = blog_kit_get_option( 'show_social_icons' );

					if ( has_nav_menu( 'primary' ) || ( 1 == $show_social_icons ) ) : ?>
						<div class="main-navigation-wrapper">
						    <?php if ( has_nav_menu( 'primary' ) ) : ?>
						    	<div id="main-nav" class="clear-fix">
							        <nav id="site-navigation" class="main-navigation" role="navigation">
							            <div class="wrap-menu-content">
											<?php
											wp_nav_menu(
												array(
												'theme_location' => 'primary',
												'menu_id'        => 'primary-menu',
												)
											);
											?>
							            </div><!-- .menu-content -->
							        </nav><!-- #site-navigation -->
						    	</div> <!-- #main-nav -->
						    <?php endif; ?>

				           <?php 
				            if ( has_nav_menu( 'social' ) && ( 1 == $show_social_icons ) ) { ?>

				    	        <div class="last-menu-item blog-kit-social-icons"> 
				    	           <?php 
				                    wp_nav_menu( array(
				                       'theme_location' => 'social',
				                       'link_before'    => '<span class="screen-reader-text">',
				                       'link_after'     => '</span>',
				                       'depth'          => 1,
				                    ) ); 
				                   ?>
				    	        </div>
				    	        <?php 
				    	    } ?>
						</div>
					<?php endif; ?>
					<div class="random" width="600">
						<p id="tbox" align="right">
						</p>
					</div>
				</div>
			</div>
		</div>
	</header><!-- #masthead -->

	<div id="content" class="site-content">