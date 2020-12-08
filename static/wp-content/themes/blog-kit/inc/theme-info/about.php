<?php
/**
 * About configuration
 *
 * @package Blog_Kit
 */

$config = array(
	'menu_name' => esc_html__( 'About Blog Kit', 'blog-kit' ),
	'page_name' => esc_html__( 'About Blog Kit', 'blog-kit' ),

	/* translators: theme version */
	'welcome_title' => sprintf( esc_html__( 'Welcome to %s - ', 'blog-kit' ), 'Blog Kit' ),

	/* translators: 1: theme name */
	'welcome_content' => esc_html__( 'Blog Kit is a simple, clean and lightweight blog theme compatible with elementor page builder.', 'blog-kit' ),

	// Quick links.
	'quick_links' => array(
		'theme_url' => array(
			'text' => esc_html__( 'Theme Details','blog-kit' ),
			'url'  => 'https://wpcharms.com/item/blog-kit/',
			),
		'demo_url' => array(
			'text' => esc_html__( 'View Demos','blog-kit' ),
			'url'  => 'https://demo.wpcharms.com/blog-kit/',
			),
		'documentation_url' => array(
			'text'   => esc_html__( 'View Documentation','blog-kit' ),
			'url'    => 'https://wpcharms.com/documentation/blog-kit/',
			),
		'rate_url' => array(
			'text' => esc_html__( 'Rate This Theme','blog-kit' ),
			'url'  => 'https://wordpress.org/support/theme/blog-kit/reviews/',
			),
		'pro_url' => array(
			'text' => esc_html__( 'Upgrade To Pro Theme','blog-kit' ),
			'url'  => 'https://wpcharms.com/item/blog-kit-pro/',
			'button' => 'primary',
			),
		),

	// Tabs.
	'tabs' => array(
		'getting_started'     => esc_html__( 'Getting Started', 'blog-kit' ),
		'recommended_actions' => esc_html__( 'Recommended Actions', 'blog-kit' ),
		'demo_content'        => esc_html__( 'Demo Content', 'blog-kit' ),
		'free_pro'            => esc_html__( 'FREE VS. PRO', 'blog-kit' ),
	),

	// Getting started.
	'getting_started' => array(
		array(
			'title'               => esc_html__( 'Theme Documentation', 'blog-kit' ),
			'text'                => esc_html__( 'Find step by step instructions with video documentation to setup theme easily.', 'blog-kit' ),
			'button_label'        => esc_html__( 'View documentation', 'blog-kit' ),
			'button_link'         => 'https://wpcharms.com/documentation/blog-kit/',
			'is_button'           => false,
			'recommended_actions' => false,
			'is_new_tab'          => true,
		),
		array(
			'title'               => esc_html__( 'Recommended Actions', 'blog-kit' ),
			'text'                => esc_html__( 'We recommend few steps to take so that you can get complete site like shown in demo.', 'blog-kit' ),
			'button_label'        => esc_html__( 'Check recommended actions', 'blog-kit' ),
			'button_link'         => esc_url( admin_url( 'themes.php?page=blog-kit-about&tab=recommended_actions' ) ),
			'is_button'           => false,
			'recommended_actions' => false,
			'is_new_tab'          => false,
		),
		array(
			'title'               => esc_html__( 'Customize Everything', 'blog-kit' ),
			'text'                => esc_html__( 'Start customizing every aspect of the website with customizer.', 'blog-kit' ),
			'button_label'        => esc_html__( 'Go to Customizer', 'blog-kit' ),
			'button_link'         => esc_url( wp_customize_url() ),
			'is_button'           => true,
			'recommended_actions' => false,
			'is_new_tab'          => false,
		),

		array(
			'title'        			=> esc_html__( 'Pro Version', 'blog-kit' ),
			'text'         			=> esc_html__( 'Upgrade to pro version for additional features and options.', 'blog-kit' ),
			'button_label' 			=> esc_html__( 'View Pro Version', 'blog-kit' ),
			'button_link'  			=> 'https://wpcharms.com/item/blog-kit-pro/',
			'is_button'    			=> true,
			'recommended_actions' 	=> false,
			'is_new_tab'   			=> true,
		),

		array(
			'title'        			=> esc_html__( 'Contact Support', 'blog-kit' ),
			'text'         			=> esc_html__( 'If you have any problem, feel free to create ticket on our dedicated Support forum.', 'blog-kit' ),
			'button_label' 			=> esc_html__( 'Contact Support', 'blog-kit' ),
			'button_link'  			=> esc_url( 'https://wpcharms.com/support/item/blog-kit/' ),
			'is_button'    			=> false,
			'recommended_actions' 	=> false,
			'is_new_tab'   			=> true,
		),

		array(
			'title'        			=> esc_html__( 'Customization Request', 'blog-kit' ),
			'text'         			=> esc_html__( 'We have dedicated team members for theme customization. Feel free to contact us any time if you need any customization service.', 'blog-kit' ),
			'button_label' 			=> esc_html__( 'Customization Request', 'blog-kit' ),
			'button_link'  			=> 'https://wpcharms.com/contact/',
			'is_button'    			=> false,
			'recommended_actions' 	=> false,
			'is_new_tab'   			=> true,
		),
	),

	// Recommended actions.
	'recommended_actions' => array(
		'content' => array(
			'one-click-demo-import' => array(
				'title'       => esc_html__( 'One Click Demo Import', 'blog-kit' ),
				'description' => esc_html__( 'Please install the One Click Demo Import plugin to import the demo content. After activation go to Appearance >> Import Demo Data and import it.', 'blog-kit' ),
				'check'       => class_exists( 'OCDI_Plugin' ),
				'plugin_slug' => 'one-click-demo-import',
				'id'          => 'one-click-demo-import',
			),
		),
	),

	// Demo content.
	'demo_content' => array(
		'description' => sprintf( esc_html__( 'Install %1$s plugin to import demo content. Demo data are bundled within the theme, Please make sure plugin is installed and activated. After plugin activation, go to Import Demo Data menu under Appearance and import it.', 'blog-kit' ), '<a href="https://wordpress.org/plugins/one-click-demo-import/" target="_blank">' . esc_html__( 'One Click Demo Import', 'blog-kit' ) . '</a>' ),
		),

    // Free vs pro array.
    'free_pro' => array(
	    array(
		    'title'     => esc_html__( 'Elementor Page Builder Compatible', 'blog-kit' ),
		    'desc'      => esc_html__( 'Works perfectly with Elementor page builder plugin', 'blog-kit' ),
		    'free'      => esc_html__('yes','blog-kit'),
		    'pro'       => esc_html__('yes','blog-kit'),
	    ),
	    array(
		    'title'     => esc_html__( 'Show/Hide Social Icons', 'blog-kit' ),
		    'desc'      => esc_html__( 'Option to show or hide social icons after menu items at header', 'blog-kit' ),
		    'free'      => esc_html__('yes','blog-kit'),
		    'pro'       => esc_html__('yes','blog-kit'),
	    ),
        array(
    	    'title'     => esc_html__( 'Multiple Blog Post Structure', 'blog-kit' ),
    	    'desc'      => esc_html__( 'Option to display blog post(archives) in two different styles', 'blog-kit' ),
    	    'free'      => esc_html__('no','blog-kit'),
    	    'pro'       => esc_html__('yes','blog-kit'),
        ),

        array(
    	    'title'     => esc_html__( 'Multiple Single Post Structure', 'blog-kit' ),
    	    'desc'      => esc_html__( 'Option to display sinlge post in two different styles', 'blog-kit' ),
    	    'free'      => esc_html__('no','blog-kit'),
    	    'pro'       => esc_html__('yes','blog-kit'),
        ),
        array(
    	    'title'     => esc_html__( 'Blog Post Meta Options', 'blog-kit' ),
    	    'desc'      => esc_html__( 'Option to show/hide meta options like posted date, author, categories, etc only for archives', 'blog-kit' ),
    	    'free'      => esc_html__('no','blog-kit'),
    	    'pro'       => esc_html__('yes','blog-kit'),
        ),
        array(
    	    'title'     => esc_html__( 'Single Post Meta Options', 'blog-kit' ),
    	    'desc'      => esc_html__( 'Option to show/hide meta options like posted date, author, categories, tags, etc only for single post', 'blog-kit' ),
    	    'free'      => esc_html__('no','blog-kit'),
    	    'pro'       => esc_html__('yes','blog-kit'),
        ),
        array(
		    'title'     => esc_html__( 'Google Fonts', 'blog-kit' ),
		    'desc' 		=> esc_html__( 'Google fonts options for changing the overall site fonts', 'blog-kit' ),
		    'free'  	=> 'no',
		    'pro'   	=> esc_html__('100+','blog-kit'),
	    ),
	    array(
		    'title'     => esc_html__( 'Color Options', 'blog-kit' ),
		    'desc'      => esc_html__( 'Option to change primary and secondary color of the site', 'blog-kit' ),
		    'free'      => esc_html__('no','blog-kit'),
		    'pro'       => esc_html__('yes','blog-kit'),
	    ),
        array(
    	    'title'     => esc_html__( 'Hide or Override Footer Credit', 'blog-kit' ),
    	    'desc'      => esc_html__( 'Option to Override existing Powerby credit of the footer or remove it', 'blog-kit' ),
    	    'free'      => esc_html__('no','blog-kit'),
    	    'pro'       => esc_html__('yes','blog-kit'),
        ),
	    array(
		    'title'     => esc_html__( 'SEO', 'blog-kit' ),
		    'desc' 		=> esc_html__( 'Developed with high skilled SEO tools.', 'blog-kit' ),
		    'free'  	=> 'yes',
		    'pro'   	=> 'yes',
	    ),
	    array(
		    'title'     => esc_html__( 'Support Forum', 'blog-kit' ),
		    'desc'      => esc_html__( 'Highly experienced and dedicated support team for your help plus online chat.', 'blog-kit' ),
		    'free'      => esc_html__('yes', 'blog-kit'),
		    'pro'       => esc_html__('High Priority', 'blog-kit'),
	    )

    ),

);
Blog_Kit_About::init( apply_filters( 'blog_kit_about_filter', $config ) );
