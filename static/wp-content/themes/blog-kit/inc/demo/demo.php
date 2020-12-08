<?php
/**
 * Demo configuration
 *
 * @package Blog_Kit
 */

$config = array(
	'static_page'    => 'home',
	'posts_page'     => 'blog',
	'menu_locations' => array(
		'primary' => 'main-menu',
		'social'  => 'social-menu',
	),
	'ocdi'           => array(
		array(
			'import_file_name'             => esc_html__( 'Default', 'blog-kit' ),
			'local_import_file'            => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/default/content.xml',
			'local_import_widget_file'     => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/default/widgets.wie',
			'local_import_customizer_file' => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/default/customizer.dat',
			'import_preview_image_url'   => trailingslashit( get_template_directory_uri() ) . 'inc/demo/demo-content/default/default.png',
			'preview_url'                => 'https://demo.wpcharms.com/blog-kit/default/',
		),
		array(
			'import_file_name'             => esc_html__( 'Elementor Version', 'blog-kit' ),
			'local_import_file'            => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/elementor/content.xml',
			'local_import_widget_file'     => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/elementor/widgets.wie',
			'local_import_customizer_file' => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/elementor/customizer.dat',
			'import_preview_image_url'   => trailingslashit( get_template_directory_uri() ) . 'inc/demo/demo-content/elementor/elementor.png',
			'preview_url'                => 'https://demo.wpcharms.com/blog-kit/elementor/',
		),
		array(
			'import_file_name'             => esc_html__( 'Gutenberg Version', 'blog-kit' ),
			'local_import_file'            => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/gutenberg/content.xml',
			'local_import_widget_file'     => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/gutenberg/widgets.wie',
			'local_import_customizer_file' => trailingslashit( get_template_directory() ) . 'inc/demo/demo-content/gutenberg/customizer.dat',
			'import_preview_image_url'   => trailingslashit( get_template_directory_uri() ) . 'inc/demo/demo-content/gutenberg/gutenberg.png',
			'preview_url'                => 'https://demo.wpcharms.com/blog-kit/gutenberg/',			
		),
	),
);

Blog_Kit_Demo::init( apply_filters( 'blog_kit_demo_filter', $config ) );
