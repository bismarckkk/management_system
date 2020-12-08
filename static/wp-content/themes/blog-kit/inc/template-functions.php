<?php
/**
 * Functions which enhance the theme by hooking into WordPress
 *
 * @package Blog_Kit
 */

/**
 * Adds custom classes to the array of body classes.
 *
 * @param array $classes Classes for the body element.
 * @return array
 */
function blog_kit_body_classes( $classes ) {
	// Adds a class of hfeed to non-singular pages.
	if ( ! is_singular() ) {
		$classes[] = 'hfeed';
	}

	// Add class for global layout.
	$global_layout = blog_kit_get_option( 'global_layout' );
	$global_layout = apply_filters( 'blog_kit_filter_global_layout', $global_layout );
	$classes[] = 'global-layout-' . esc_attr( $global_layout );

	return $classes;
}
add_filter( 'body_class', 'blog_kit_body_classes' );

/**
 * Add a pingback url auto-discovery header for single posts, pages, or attachments.
 */
function blog_kit_pingback_header() {
	if ( is_singular() && pings_open() ) {
		echo '<link rel="pingback" href="', esc_url( get_bloginfo( 'pingback_url' ) ), '">';
	}
}
add_action( 'wp_head', 'blog_kit_pingback_header' );

if ( ! function_exists( 'blog_kit_fonts_url' ) ) :

	/**
	 * Register Google fonts.
	 *
	 * @since 1.0.0
	 *
	 * @return string Google fonts URL for the theme.
	 */
	function blog_kit_fonts_url() {
		$fonts_url = '';
		$fonts     = array();
		$subsets   = 'latin,latin-ext';

		/* translators: If there are characters in your language that are not supported by Work Sans, translate this to 'off'. Do not translate into your own language. */

		if ( 'off' !== _x( 'on', 'Roboto font: on or off', 'blog-kit' ) ) {
			$fonts[] = 'Roboto:400,400i,500,500i,700,700i';
		}

		if ( $fonts ) {
			$fonts_url = add_query_arg( array(
				'family' => urlencode( implode( '|', $fonts ) ),
				'subset' => urlencode( $subsets ),
			), '//fonts.googleapis.com/css' );
		}

		return $fonts_url;
	}

endif;

//=============================================================
// Function to change default excerpt
//=============================================================
if ( ! function_exists( 'blog_kit_implement_excerpt_length' ) ) :

	/**
	 * Implement excerpt length.
	 *
	 * @since 1.0.0
	 *
	 * @param int $length The number of words.
	 * @return int Excerpt length.
	 */
	function blog_kit_implement_excerpt_length( $length ) {

		$excerpt_length = blog_kit_get_option( 'excerpt_length' );

		if ( absint( $excerpt_length ) > 0 ) {
			$length = absint( $excerpt_length );
		}
		return $length;

	}
endif;

if ( ! function_exists( 'blog_kit_content_more_link' ) ) :

	/**
	 * Implement read more in content.
	 *
	 * @since 1.0.0
	 *
	 * @param string $more_link Read More link element.
	 * @param string $more_link_text Read More text.
	 * @return string Link.
	 */
	function blog_kit_content_more_link( $more_link, $more_link_text ) {

		$read_more_text = blog_kit_get_option('readmore_text');

		if ( ! empty( $read_more_text ) ) {

			$more_link = str_replace( $more_link_text, esc_html( $read_more_text ), $more_link );

		}

		return $more_link;

	}

endif;

if ( ! function_exists( 'blog_kit_implement_read_more' ) ) :

	/**
	 * Implement read more in excerpt.
	 *
	 * @since 1.0.0
	 *
	 * @param string $more The string shown within the more link.
	 * @return string The excerpt.
	 */
	function blog_kit_implement_read_more( $more ) {

		$output = $more;

		$read_more_text = blog_kit_get_option('readmore_text');

		if ( ! empty( $read_more_text ) ) {

			$output = '&hellip;<p><a href="' . esc_url( get_permalink() ) . '" class="btn-more">' . esc_html( $read_more_text ) . '<span class="arrow-more">&rarr;</span></a></p>';

		}

		return $output;

	}
endif;

if ( ! function_exists( 'blog_kit_hook_read_more_filters' ) ) :

	/**
	 * Hook read more and excerpt length filters.
	 *
	 * @since 1.0.0
	 */
	function blog_kit_hook_read_more_filters() {
		
		add_filter( 'excerpt_length', 'blog_kit_implement_excerpt_length', 999 );
		add_filter( 'the_content_more_link', 'blog_kit_content_more_link', 10, 2 );
		add_filter( 'excerpt_more', 'blog_kit_implement_read_more' );

	}
endif;
add_action( 'wp', 'blog_kit_hook_read_more_filters' );

if ( ! function_exists( 'blog_kit_get_option' ) ) :

    /**
     * Get theme option.
     *
     * @since 1.0.0
     *
     * @param string $key Option key.
     * @return mixed Option value.
     */
    function blog_kit_get_option( $key ) {

        if ( empty( $key ) ) {

            return;

        }

        //default theme options
        $defaults = array();
        $defaults['site_identity'] 		= 'title-text';
        $defaults['show_social_icons'] 	= false;
        $defaults['global_layout'] 	= 'right-sidebar';
        $defaults['excerpt_length'] = 40;
        $defaults['readmore_text'] 	= esc_html__( 'Read More', 'blog-kit' );
        $defaults['copyright_text'] = esc_html__( 'Copyright © All rights reserved.', 'blog-kit' );

        //get theme options and use default if theme option not set
        $theme_options = get_theme_mod( 'theme_options', $defaults );
        $theme_options = array_merge( $defaults, $theme_options );
        $value = '';

        if ( isset( $theme_options[ $key ] ) ) {
            $value = $theme_options[ $key ];
        }

        return $value;

    }

endif;

if ( ! function_exists( 'blog_kit_plugins_recommendation' ) ) :

function blog_kit_plugins_recommendation() {
	
	$plugins = array(
		array(
			'name'     => esc_html__( 'One Click Demo Import', 'blog-kit' ),
			'slug'     => 'one-click-demo-import',
			'required' => false,
		),
		array(
			'name'     => esc_html__( 'Elementor Page Builder', 'blog-kit' ),
			'slug'     => 'elementor',
			'required' => false,
		),
		array(
			'name'     => esc_html__( 'Post Grid Elementor Addon', 'blog-kit' ),
			'slug'     => 'post-grid-elementor-addon',
			'required' => false,
		),
		array(
			'name'     => esc_html__( 'Add Instagram Feed For Elementor', 'blog-kit' ),
			'slug'     => 'add-instagram-feed-for-elementor',
			'required' => false,
		),
	);

	tgmpa( $plugins );
}
endif;
add_action( 'tgmpa_register', 'blog_kit_plugins_recommendation' );

//=============================================================
// Body open hook
//=============================================================
if ( ! function_exists( 'wp_body_open' ) ) {
    /**
     * Body open hook.
     */
    function wp_body_open() {
        do_action( 'wp_body_open' );
    }
}