<?php
/**
 * Blog Kit Theme Customizer
 *
 * @package Blog_Kit
 */

/**
 * Add postMessage support for site title and description for the Theme Customizer.
 *
 * @param WP_Customize_Manager $wp_customize Theme Customizer object.
 */
function blog_kit_customize_register( $wp_customize ) {

	$wp_customize->get_setting( 'blogname' )->transport         = 'postMessage';
	$wp_customize->get_setting( 'blogdescription' )->transport  = 'postMessage';
	$wp_customize->get_setting( 'header_textcolor' )->transport = 'postMessage';

	if ( isset( $wp_customize->selective_refresh ) ) {
		$wp_customize->selective_refresh->add_partial( 'blogname', array(
			'selector'        		=> '.site-title a',
			'container_inclusive' 	=> false,
			'render_callback' 	    => 'blog_kit_customize_partial_blogname',
		) );
		$wp_customize->selective_refresh->add_partial( 'blogdescription', array(
			'selector'        		=> '.site-description',
			'container_inclusive' 	=> false,
			'render_callback' 		=> 'blog_kit_customize_partial_blogdescription',
		) );
	}

	// Sanitization.
	require_once trailingslashit( get_template_directory() ) . '/inc/sanitize.php';

	// Load Upgrade to Pro control.
	require_once trailingslashit( get_template_directory() ) . '/inc/upgrade-to-pro/control.php';

	// Register custom section types.
	$wp_customize->register_section_type( 'Blog_Kit_Customize_Section_Upsell' );

	// Register sections.
	$wp_customize->add_section(
		new Blog_Kit_Customize_Section_Upsell(
			$wp_customize,
			'theme_upsell',
			array(
				'title'    => esc_html__( 'Blog Kit Pro', 'blog-kit' ),
				'pro_text' => esc_html__( 'BUY PRO', 'blog-kit' ),
				'pro_url'  => 'https://wpcharms.com/item/blog-kit-pro/',
				'priority' => 1,
			)
		)
	);

	//Logo Options Setting Starts
	$wp_customize->add_setting('theme_options[site_identity]', 
		array(
			'default' 			=> 'title-text',
			'sanitize_callback' => 'blog_kit_sanitize_select'
		)
	);

	$wp_customize->add_control('theme_options[site_identity]', 
		array(
			'type' 		=> 'radio',
			'label' 	=> esc_html__('Logo Options', 'blog-kit'),
			'section' 	=> 'title_tagline',
			'choices' 	=> array(
				'logo-only' 	=> esc_html__('Logo Only', 'blog-kit'),
				'title-only' 	=> esc_html__('Title Only', 'blog-kit'),
				'title-text' 	=> esc_html__('Title + Tagline', 'blog-kit'),
				)
		)
	);
	
	// Add Theme Options Panel.
	$wp_customize->add_panel( 'theme_option_panel',
		array(
			'title'      => esc_html__( 'Theme Options', 'blog-kit' ),
			'priority'   => 100,
		)
	);

	// Header Section.
	$wp_customize->add_section( 'section_header',
		array(
			'title'      => esc_html__( 'Header', 'blog-kit' ),
			'priority'   => 100,
			'panel'      => 'theme_option_panel',
		)
	);

	// Setting show_social_icons.
	$wp_customize->add_setting( 'theme_options[show_social_icons]',
		array(
			'default'           => false,
			'sanitize_callback' => 'blog_kit_sanitize_checkbox',
		)
	);
	$wp_customize->add_control( 'theme_options[show_social_icons]',
		array(
			'label'    => esc_html__( 'Show Social Icons', 'blog-kit' ),
			'section'  => 'section_header',
			'type'     => 'checkbox',
			'priority' => 100,
		)
	);

	// Layout Section.
	$wp_customize->add_section( 'section_layout',
		array(
			'title'      => esc_html__( 'Layouts', 'blog-kit' ),
			'priority'   => 100,
			'panel'      => 'theme_option_panel',
		)
	);

	// Setting global_layout.
	$wp_customize->add_setting( 'theme_options[global_layout]',
		array(
			'default'           => 'right-sidebar',
			'sanitize_callback' => 'blog_kit_sanitize_select',
		)
	);
	$wp_customize->add_control( 'theme_options[global_layout]',
		array(
			'label'    => esc_html__( 'Default Sidebar Layout', 'blog-kit' ),
			'section'  => 'section_layout',
			'type'     => 'radio',
			'priority' => 100,
			'choices'  => array(
					'left-sidebar'  => esc_html__( 'Sidebar / Content', 'blog-kit' ),
					'right-sidebar' => esc_html__( 'Content / Sidebar', 'blog-kit' ),
				),
		)
	);

	// Setting excerpt_length.
	$wp_customize->add_setting( 'theme_options[excerpt_length]',
		array(
			'default'           => 40,
			'sanitize_callback' => 'absint',
		)
	);
	$wp_customize->add_control( 'theme_options[excerpt_length]',
		array(
			'label'       => esc_html__( 'Excerpt Length', 'blog-kit' ),
			'section'     => 'section_layout',
			'type'        => 'number',
			'priority'    => 100,
			'input_attrs' => array( 'min' => 1, 'max' => 500, 'style' => 'width: 55px;' ),
		)
	);

	// Setting readmore_text.
	$wp_customize->add_setting( 'theme_options[readmore_text]',
		array(
			'default'           => esc_html__( 'Read More', 'blog-kit' ),
			'sanitize_callback' => 'sanitize_text_field',
		)
	);
	$wp_customize->add_control( 'theme_options[readmore_text]',
		array(
			'label'    => esc_html__( 'Read More Text', 'blog-kit' ),
			'section'  => 'section_layout',
			'type'     => 'text',
			'priority' => 100,
		)
	);

	// Footer Section.
	$wp_customize->add_section( 'section_footer',
		array(
			'title'      => esc_html__( 'Footer', 'blog-kit' ),
			'priority'   => 100,
			'panel'      => 'theme_option_panel',
		)
	);

	// Setting copyright_text.
	$wp_customize->add_setting( 'theme_options[copyright_text]',
		array(
			'default'           => esc_html__( 'Copyright © All rights reserved.', 'blog-kit' ),
			'sanitize_callback' => 'sanitize_text_field',
		)
	);
	$wp_customize->add_control( 'theme_options[copyright_text]',
		array(
			'label'    => esc_html__( 'Copyright Text', 'blog-kit' ),
			'section'  => 'section_footer',
			'type'     => 'text',
			'priority' => 100,
		)
	);

}

add_action( 'customize_register', 'blog_kit_customize_register' );

/**
 * Render the site title for the selective refresh partial.
 *
 * @return void
 */
function blog_kit_customize_partial_blogname() {
	bloginfo( 'name' );
}

/**
 * Render the site tagline for the selective refresh partial.
 *
 * @return void
 */
function blog_kit_customize_partial_blogdescription() {
	bloginfo( 'description' );
}

/**
 * Enqueue style for custom customize control.
 */
function blog_kit_custom_customizer_scripts() {

	wp_enqueue_script( 'blog-kit-customize-controls', get_template_directory_uri() . '/inc/upgrade-to-pro/customize-controls.js', array( 'customize-controls' ) );

	wp_enqueue_style( 'blog-kit-customize-controls', get_template_directory_uri() . '/inc/upgrade-to-pro/customize-controls.css' );
}
add_action( 'customize_controls_enqueue_scripts', 'blog_kit_custom_customizer_scripts' );