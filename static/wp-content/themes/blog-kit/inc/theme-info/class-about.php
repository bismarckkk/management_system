<?php
/**
 * About class
 *
 * @package Blog_Kit
 */

if ( ! class_exists( 'Blog_Kit_About' ) ) {

	/**
	 * Main class.
	 *
	 * @since 1.0.0
	 */
	class Blog_Kit_About {

		/**
		 * Class version.
		 *
		 * @var string $version Version.
		 */
		private $version = '1.0.0';

		/**
		 * Page configuration.
		 *
		 * @var array $config Configuration.
		 */
		private $config;

		/**
		 * Theme name.
		 *
		 * @var string $theme_name Theme name.
		 */
		private $theme_name;

		/**
		 * Logo image URL.
		 *
		 * @var string $logo_url Logo image URL.
		 */
		private $logo_url;

		/**
		 * Logo link.
		 *
		 * @var string $logo_link Logo link.
		 */
		private $logo_link;

		/**
		 * Theme slug.
		 *
		 * @var string $theme_slug Theme slug.
		 */
		private $theme_slug;

		/**
		 * Current theme object.
		 *
		 * @var WP_Theme $theme Current theme.
		 */
		private $theme;

		/**
		 * Theme version.
		 *
		 * @var string $theme_version Theme version.
		 */
		private $theme_version;

		/**
		 * Admin menu name.
		 *
		 * @var string $menu_name Menu name under Appearance.
		 */
		private $menu_name;

		/**
		 * Page title.
		 *
		 * @var string $page_name Title of the about page.
		 */
		private $page_name;

		/**
		 * Page slug.
		 *
		 * @var string $page_slug Slug of about page.
		 */
		private $page_slug;

		/**
		 * Recommended action option key.
		 *
		 * @var string $action_option_key Action key.
		 */
		private $action_key;

		/**
		 * Page tabs.
		 *
		 * @var array $tabs Page tabs.
		 */
		private $tabs;

		/**
		 * HTML notification content displayed upon activation.
		 *
		 * @var string $notification HTML notification content.
		 */
		private $notification;

		/**
		 * Singleton instance of Blog_Kit_About.
		 *
		 * @var Blog_Kit_About $instance Blog_Kit_About instance.
		 */
		private static $instance;

		/**
		 * Main Blog_Kit_About instance.
		 *
		 * @since 1.0.0
		 *
		 * @param array $config Configuration array.
		 */
		public static function init( $config ) {
			if ( ! isset( self::$instance ) && ! ( self::$instance instanceof Blog_Kit_About ) ) {
				self::$instance = new Blog_Kit_About;
				if ( ! empty( $config ) && is_array( $config ) ) {
					self::$instance->config = $config;
					self::$instance->setup_config();
					self::$instance->setup_actions();
				}
			}
		}

		/**
		 * Setup the class props based on the config array.
		 *
		 * @since 1.0.0
		 */
		public function setup_config() {
			$theme = wp_get_theme();
			if ( is_child_theme() ) {
				$this->theme_name = $theme->parent()->get( 'Name' );
				$this->theme      = $theme->parent();
			} else {
				$this->theme_name = $theme->get( 'Name' );
				$this->theme      = $theme->parent();
			}

			$this->theme_version = $theme->get( 'Version' );
			$this->theme_slug    = $theme->get_template();
			$this->page_slug     = $this->theme_slug . '-about';
			$this->action_key    = $this->theme_slug . '-recommended_actions';
			$this->menu_name     = isset( $this->config['menu_name'] ) ? $this->config['menu_name'] : $this->theme_name;
			$this->page_name     = isset( $this->config['page_name'] ) ? $this->config['page_name'] : $this->theme_name;
			$this->logo_url      = isset( $this->config['logo_url'] ) ? $this->config['logo_url'] : get_template_directory_uri() . '/inc/theme-info/images/wpcharms.png';
			$this->logo_link     = isset( $this->config['logo_link'] ) ? $this->config['logo_link'] : 'https://wpcharms.com/';
			$this->tabs          = isset( $this->config['tabs'] ) ? $this->config['tabs'] : array();
			$this->notification  = isset( $this->config['notification'] ) ? $this->config['notification'] : ( '<p>' . sprintf( esc_html__( 'Welcome! Thank you for choosing %1$s! To fully take advantage of the best our theme can offer please make sure you visit our %2$swelcome page%3$s.', 'blog-kit' ), $this->theme_name, '<a href="' . esc_url( admin_url( 'themes.php?page=' . $this->page_slug ) ) . '">', '</a>' ) . '</p><p><a href="' . esc_url( admin_url( 'themes.php?page=' . $this->page_slug ) ) . '" class="button button-primary" style="text-decoration: none;">' . sprintf( esc_html__( 'Get started with %s', 'blog-kit' ), $this->theme_name ) . '</a></p>' );
		}

		/**
		 * Setup actions.
		 *
		 * @since 1.0.0
		 */
		public function setup_actions() {
			add_action( 'admin_menu', array( $this, 'register' ) );
			add_action( 'load-themes.php', array( $this, 'activation_admin_notice' ) );
			add_action( 'admin_enqueue_scripts', array( $this, 'load_assets' ) );
			add_action( 'wp_ajax_wpcap_about_action_dismiss_recommended_action', array( $this, 'dismiss_recommended_action_callback' ) );
			add_action( 'wp_ajax_nopriv_wpcap_about_action_dismiss_recommended_action', array( $this, 'dismiss_recommended_action_callback' ) );
		}

		/**
		 * Register the page under Appearance.
		 *
		 * @since 1.0.0
		 */
		public function register() {
			if ( ! empty( $this->menu_name ) && ! empty( $this->page_name ) ) {

				$count = $this->get_total_recommended_actions();

				$title = $this->page_name;

				if ( $count > 0 ) {
					$title .= '<span class="badge-action-count">' . esc_html( $count ) . '</span>';
				}

				add_theme_page(
					$this->menu_name,
					$title,
					'edit_theme_options',
					$this->page_slug,
					array( $this, 'render_about_page' )
				);
			}
		}

		/**
		 * Get total recommended actions count.
		 *
		 * @since 1.0.0
		 *
		 * @return int Total count.
		 */
		private function get_total_recommended_actions() {
			$actions = $this->get_recommended_actions();
			return count( $actions );
		}

		/**
		 * Return valid array of recommended actions.
		 *
		 * @return array Valid array of recommended actions.
		 */
		private function get_recommended_actions() {
			$saved_actions = get_option( $this->action_key );

			if ( ! is_array( $saved_actions ) ) {
				$saved_actions = array();
			}

			$valid = array();

			$action_config = isset( $this->config['recommended_actions'] ) ? $this->config['recommended_actions'] : array();

			if ( ! empty( $action_config['content'] ) ) {
				foreach ( $action_config['content'] as $item ) {
					if ( isset( $item['check'] ) && true === $item['check'] ) {
						continue;
					}
					if ( isset( $saved_actions[ $item['id'] ] ) && false === $saved_actions[ $item['id'] ] ) {
						continue;
					}
					$valid[] = $item;
				}
			}

			return $valid;
		}

		/**
		 * Render quick links.
		 *
		 * @since 1.0.0
		 */
		public function render_quick_links() {
			$quick_links = ( isset( $this->config['quick_links'] ) ) ? $this->config['quick_links'] : array();

			if ( empty( $quick_links ) ) {
				return;
			}

			echo '<p>';
			foreach ( $quick_links as $link ) {
				$link_class = 'button';
				if ( isset( $link['button'] ) ) {
					$link_class .= ' button-' . esc_attr( $link['button'] );
				}
				echo '<a href="' . esc_url( $link['url'] ) . '" class="' . esc_attr( $link_class ) . '" target="_blank">' . esc_html( $link['text'] ) . '</a>&nbsp;&nbsp;';
			}
			echo '</p>';
		}

		/**
		 * Render main page.
		 *
		 * @since 1.0.0
		 */
		public function render_about_page() {
			if ( ! empty( $this->config['welcome_title'] ) ) {
				$welcome_title = $this->config['welcome_title'];
			}

			if ( ! empty( $this->config['welcome_content'] ) ) {
				$welcome_content = $this->config['welcome_content'];
			}

			if ( ! empty( $welcome_title ) || ! empty( $welcome_content ) || ! empty( $this->tabs ) ) {

				echo '<div class="wrap about-wrap wpcap-wrap">';

				if ( ! empty( $welcome_title ) ) {
					echo '<h1>';
					echo esc_html( $welcome_title );
					if ( ! empty( $this->theme_version ) ) {
						echo esc_html( $this->theme_version );
					}
					echo '</h1>';
				}

				if ( ! empty( $welcome_content ) ) {
					echo '<div class="about-text">' . wp_kses_post( $welcome_content ) . '</div>';
				}

				if ( $this->logo_url && $this->logo_link ) {
					echo '<a href="' . esc_url( $this->logo_link ) . '" target="_blank" class="about-logo wp-badge" style="background-image:url(' . esc_url( $this->logo_url ) . ');"></a>';
				}

				$this->render_quick_links();

				// Display tabs.
				if ( ! empty( $this->tabs ) ) {
					$active_tab = isset( $_GET['tab'] ) ? wp_unslash( $_GET['tab'] ) : 'getting_started';

					echo '<h2 class="nav-tab-wrapper wp-clearfix">';

					foreach ( $this->tabs as $tab_key => $tab_name ) {

						if ( 'useful_plugins' === $tab_key ) {
							global $tgmpa;
							if ( ! isset( $tgmpa ) ) {
								continue;
							}
						}

						echo '<a href="' . esc_url( admin_url( 'themes.php?page=' . $this->page_slug ) ) . '&tab=' . $tab_key . '" class="nav-tab ' . ( $active_tab === $tab_key ? 'nav-tab-active' : '' ) . '" role="tab" data-toggle="tab">';

						if ( 'upgrade_to_pro' === $tab_key ) {
							echo '<span class="dashicons dashicons-star-filled"></span>';
						}

						echo esc_html( $tab_name );

						if ( 'recommended_actions' === $tab_key ) {
							$count = $this->get_total_recommended_actions();
							if ( $count > 0 ) {
								echo '<span class="badge-action-count">' . esc_html( $count ) . '</span>';
							}
						}

						echo '</a>';
					}

					echo '</h2>';

					// Display content for current tab.
					if ( method_exists( $this, $active_tab ) ) {
						$this->$active_tab();
					}
				} // End if().

				echo '</div><!--/.wrap.about-wrap-->';
			} // End if().
		}

		/**
		 * Adds an admin notice upon successful activation.
		 *
		 * @since 1.0.0
		 */
		public function activation_admin_notice() {
			global $pagenow;
			if ( is_admin() && ( 'themes.php' === $pagenow ) && isset( $_GET['activated'] ) ) {
				add_action( 'admin_notices', array( $this, 'welcome_admin_notice' ), 99 );
			}
		}

		/**
		 * Display an admin notice linking to the about page.
		 *
		 * @since 1.0.0
		 */
		public function welcome_admin_notice() {
			if ( ! empty( $this->notification ) ) {
				echo '<div class="updated notice is-dismissible">';
				echo wp_kses_post( $this->notification );
				echo '</div>';
			}
		}

		/**
		 * Load assets.
		 *
		 * @since 1.0.0
		 *
		 * @param string $hook Hook name.
		 */
		public function load_assets( $hook ) {

			$min = defined( 'SCRIPT_DEBUG' ) && SCRIPT_DEBUG ? '' : '.min';

			$custom_css = '.badge-action-count {
				padding: 0 6px;
				display: inline-block;
				background-color: #d54e21;
				color: #fff;
				font-size: 9px;
				line-height: 17px;
				font-weight: 600;
				margin: 1px 0 0 2px;
				vertical-align: top;
				border-radius: 10px;
				z-index: 26;
				margin-top: 5px;
				margin-left: 5px;
			}
			.wp-submenu .badge-action-count {
				margin-top: 0;
			}';

			wp_add_inline_style( 'admin-menu', $custom_css );

			if ( 'appearance_page_' . $this->page_slug === $hook ) {
				wp_enqueue_style( 'plugin-install' );
				wp_enqueue_script( 'plugin-install' );
				wp_enqueue_script( 'updates' );

				wp_enqueue_style( 'blog-kit-about', get_template_directory_uri() . '/inc/theme-info/css/about.css', array(), '2.0.3' );
				wp_enqueue_script( 'blog-kit-about', get_template_directory_uri() . '/inc/theme-info/js/about.js', array( 'jquery' ), '2.0.3' );
				$js_vars = array(
					'ajaxurl' => esc_url( admin_url( 'admin-ajax.php' ) ),
				);
				wp_localize_script( 'blog-kit-about', 'BlogKitAboutObject', $js_vars );
			}
		}

		/**
		 * Render getting started tab.
		 *
		 * @since 1.0.0
		 */
		public function getting_started() {
			if ( ! empty( $this->config['getting_started'] ) ) {

				$getting_started = $this->config['getting_started'];

				if ( ! empty( $getting_started ) ) {

					echo '<div class="feature-section has-3-columns alignleft">';

					foreach ( $getting_started as $getting_started_item ) {

						echo '<div class="card">';

						if ( ! empty( $getting_started_item['title'] ) ) {
							echo '<h3>' . esc_html( $getting_started_item['title'] ) . '</h3>';
						}

						if ( ! empty( $getting_started_item['text'] ) ) {
							echo '<p>' . esc_html( $getting_started_item['text'] ) . '</p>';
						}

						if ( ! empty( $getting_started_item['button_link'] ) && ! empty( $getting_started_item['button_label'] ) ) {

							echo '<p>';
							$button_class = '';
							if ( $getting_started_item['is_button'] ) {
								$button_class = 'button button-primary';
							}

							$count = $this->get_total_recommended_actions();

							if ( $getting_started_item['recommended_actions'] && isset( $count ) ) {
								if ( 0 === $count ) {
									echo '<span class="dashicons dashicons-yes"></span>';
								} else {
									echo '<span class="dashicons dashicons-no-alt"></span>';
								}
							}

							$button_new_tab = '_self';
							if ( isset( $getting_started_item['is_new_tab'] ) ) {
								if ( $getting_started_item['is_new_tab'] ) {
									$button_new_tab = '_blank';
								}
							}

							echo '<a target="' . $button_new_tab . '" href="' . esc_url( $getting_started_item['button_link'] ) . '"class="' . esc_attr( $button_class ) . '">' . esc_html( $getting_started_item['button_label'] ) . '</a>';
							echo '</p>';
						}

						echo '</div><!-- .col -->';
					} // End foreach().
					echo '</div><!-- .feature-section three-col -->';
				} // End if().
			} // End if().
		}

		/**
		 * Render recommended actions tab.
		 *
		 * @since 1.0.0
		 */
		public function recommended_actions() {
			$recommended_actions = isset( $this->config['recommended_actions'] ) ? $this->config['recommended_actions'] : array();

			if ( ! empty( $recommended_actions ) ) {

				echo '<div class="about-tab-wrapper feature-section action-recommended has-1-columns alignleft" id="plugin-filter1">';

				$actions = array();

				foreach ( $recommended_actions['content'] as $action ) {
					$actions[] = $action;
				}

				if ( ! empty( $actions ) && is_array( $actions ) ) {

					$about_recommended_actions = get_option( $this->action_key );

					foreach ( $actions as $action_key => $action_value ) {

						$hidden = false;

						if ( isset( $action_value['id'] ) && isset( $about_recommended_actions[ $action_value['id'] ] ) && ( false === $about_recommended_actions[ $action_value['id'] ] ) ) {
							$hidden = true;
						}

						$complete = false;

						if ( isset( $action_value['check'] ) && $action_value['check'] ) {
							$complete = true;
						}

						$complete_class = ( true === $complete ) ? 'complete': '';

						echo '<div class="action-recommended-box ' . esc_attr( $complete_class ) . '">';

						if ( isset( $action_value['id'] ) ) {
							$nonce = 'action-' . $action_value['id'];
							if ( ! $hidden ) {
								$nonce .= '-dismiss';
								echo '<span data-action="dismiss" data-nonce="' . esc_attr( wp_create_nonce( $nonce ) ) . '" class="dashicons dashicons-visibility recommended-action-button" id="' . esc_attr( $action_value['id'] ) . '"></span>';
							} else {
								$nonce .= '-add';
								echo '<span data-action="add" data-nonce="' . esc_attr( wp_create_nonce( $nonce ) ) . '" class="dashicons dashicons-hidden recommended-action-button" id="' . esc_attr( $action_value['id'] ) . '"></span>';
							}
						}

						if ( ! empty( $action_value['title'] ) ) {
							echo '<h3>' . wp_kses_post( $action_value['title'] ) . '</h3>';
						}

						if ( ! empty( $action_value['description'] ) ) {
							echo '<p>' . wp_kses_post( $action_value['description'] ) . '</p>';
						}

						if ( ! empty( $action_value['help'] ) ) {
							echo '<div>' . wp_kses_post( $action_value['help'] ) . '</div>';
						}

						if ( ! empty( $action_value['plugin_slug'] ) ) {

							$active = $this->check_if_plugin_active( $action_value['plugin_slug'] );
							$url    = $this->create_action_link( $active['needs'], $action_value['plugin_slug'] );

							$label = '';

							switch ( $active['needs'] ) {

								case 'install':
									$class = 'install-now button';
									$label = esc_html__( 'Install', 'blog-kit' );
									break;
								case 'activate':
									$class = 'activate-now button button-primary';
									$label = esc_html__( 'Activate', 'blog-kit' );
									break;
								case 'deactivate':
									$class = 'deactivate-now button';
									$label = esc_html__( 'Deactivate', 'blog-kit' );
									break;
							}
							?>

							<p class="plugin-card-<?php echo esc_attr( $action_value['plugin_slug'] ); ?> action_button <?php echo ( 'install' !== $active['needs'] && $active['status'] ) ? 'active' : ''; ?>">
								<a data-slug="<?php echo esc_attr( $action_value['plugin_slug'] ); ?>" class="<?php echo esc_attr( $class ); ?>" href="<?php echo esc_url( $url ); ?>"><?php echo esc_html( $label ); ?></a>
							</p>

							<?php

						} // End if().
						echo '</div>';
					} // End foreach().
				} // End if().
				echo '</div>';
			} // End if().
		}

		/**
		 * Render upgrade tab.
		 *
		 * @since 1.0.0
		 */
		public function upgrade_to_pro() {
			$upgrade_to_pro = ( isset( $this->config['upgrade_to_pro'] ) ) ? $this->config['upgrade_to_pro'] : array();

			echo '<div class="feature-section upgrade-to-pro">';

			if ( isset( $upgrade_to_pro['description'] ) && ! empty( $upgrade_to_pro['description'] ) ) {
				echo '<div>' . wp_kses_post( $upgrade_to_pro['description'] ) . '</div>';
			}

			if ( isset( $upgrade_to_pro['button_link'] ) && ! empty( $upgrade_to_pro['button_link'] ) ) {
				$button_text = esc_html__( 'Upgrade to Pro', 'blog-kit' );

				if ( isset( $upgrade_to_pro['button_label'] ) && ! empty( $upgrade_to_pro['button_label'] ) ) {
					$button_text = $upgrade_to_pro['button_label'];
				}

				$target = '_self';
				if ( isset( $upgrade_to_pro['is_new_tab'] ) && true === $upgrade_to_pro['is_new_tab'] ) {
					$target = '_blank';
				}

				echo '<a href="' . esc_url( $upgrade_to_pro['button_link'] ) . '" class="button button-primary" target="' . esc_attr( $target ) . '">' . esc_html( $button_text ) . '</a>';
			}

			echo '</div>';

		}

		/**
		 * Render demo content.
		 *
		 * @since 1.0.0
		 */
		public function demo_content() {
			$demo_content = ( isset( $this->config['demo_content'] ) ) ? $this->config['demo_content'] : array();

			echo '<div class="feature-section demo-content has-1-columns alignleft">';

			if ( isset( $demo_content['description'] ) && ! empty( $demo_content['description'] ) ) {
				echo '<div class="card"><p>' . wp_kses_post( $demo_content['description'] ) . '</p></div>';
			}

			echo '</div>';
		}

		/**
		 * Free vs PRO tab
		 */
		public function free_pro() {
		    $free_pro = isset( $this->config['free_pro'] ) ? $this->config['free_pro'] : array();
		    if ( ! empty( $free_pro ) ) {
		        /*defaults values for child theme array */
		        $defaults = array(
		            'title'=> '',
		            'desc' => '',
		            'free' => '',
		            'pro'  => '',
		        );

		        if ( ! empty( $free_pro ) && is_array( $free_pro ) ) {
		            echo '<div class="feature-section charm-free-pro">';
		            echo '<div id="free_pro" class="at-theme-info-tab-pane at-theme-info-fre-pro">';
		            echo '<table class="free-pro-table">';
		            echo '<thead>';
		            echo '<tr>';
		            echo '<th></th>';
		            echo '<th>' . esc_html__( 'Blog Kit','blog-kit' ) . '</th>';
		            echo '<th>' . esc_html__( 'Blog Kit Pro','blog-kit' ) . '</th>';
		            echo '</tr>';
		            echo '</thead>';
		            echo '<tbody>';
		            foreach ( $free_pro as $feature ) {

		                $instance = wp_parse_args( (array) $feature, $defaults );

		                /*allowed 7 value in array */
		                $title = $instance[ 'title' ];
		                $desc = $instance[ 'desc'];
		                $free = $instance[ 'free'];
		                $pro = $instance[ 'pro'];

		                echo '<tr>';
		                if ( ! empty( $title ) || ! empty( $desc ) ) {
		                    echo '<td>';
		                    if ( ! empty( $title ) ) {
		                        echo '<h3>' . wp_kses_post( $title ) . '</h3>';
		                    }
		                    if ( ! empty( $desc ) ) {
		                        echo '<p>' . wp_kses_post( $desc ) . '</p>';
		                    }
		                    echo '</td>';
		                }

		                if ( ! empty( $free )) {
		                    if( 'yes' === $free ){
		                        echo '<td class="only-lite"><span class="dashicons-before dashicons-yes"></span></td>';
		                    }
		                    elseif ( 'no' === $free ){
		                        echo '<td class="only-pro"><span class="dashicons-before dashicons-no-alt"></span></td>';
		                    }
		                    else{
		                        echo '<td class="only-lite">'.esc_html($free ).'</td>';
		                    }

		                }
		                if ( ! empty( $pro )) {
		                    if( 'yes' === $pro ){
		                        echo '<td class="only-lite"><span class="dashicons-before dashicons-yes"></span></td>';
		                    }
		                    elseif ( 'no' === $pro ){
		                        echo '<td class="only-pro"><span class="dashicons-before dashicons-no-alt"></span></td>';
		                    }
		                    else{
		                        echo '<td class="only-lite">'.esc_html($pro ).'</td>';
		                    }
		                }
		                echo '</tr>';
		            }

		            echo '<tr class="wpcap-theme-info-text-center">';
		            echo '<td></td>';
		            echo '<td colspan="2"><a href="https://wpcharms.com/item/blog-kit-pro/" target="_blank" class="button button-primary button-hero">Blog Kit Pro</a></td>';
		            echo '</tr>';

		            echo '</tbody>';
		            echo '</table>';
		            echo '</div>';
		            echo '</div>';

		        }
		    }
		}

		/**
		 * Check if plugin is active.
		 *
		 * @since 1.0.0
		 *
		 * @param string $slug Plugin slug.
		 * @return array Status detail.
		 */
		public function check_if_plugin_active( $slug ) {

			$output = array(
				'status' => null,
				'needs'  => null,
				);

			$is_installed = $this->is_plugin_installed( $slug );

			if ( true === $is_installed ) {
				// Installed.
				$status = $this->is_plugin_active( $slug );
				if ( false === $status ) {
					// Plugin is inactive.
					$output = array(
						'status' => $status,
						'needs'  => 'activate',
						);
				} else {
					// Plugin is active.
					$output = array(
						'status' => $status,
						'needs'  => 'deactivate',
						);
				}
			} else {
				// Not installed.
				$output = array(
					'status' => false,
					'needs'  => 'install',
					);
			}

			return $output;
		}

		/**
		 * Create action link.
		 *
		 * @since 1.0.0
		 *
		 * @param string $state State.
		 * @param string $slug  Plugin slug.
		 * @return string Plugin detail.
		 */
		public function create_action_link( $state, $slug ) {
			$file_path = $this->get_plugin_basename_from_slug( $slug );

			switch ( $state ) {
				case 'install':
					$action_url = wp_nonce_url(
						add_query_arg(
							array(
								'action' => 'install-plugin',
								'plugin' => $slug,
							),
							network_admin_url( 'update.php' )
						),
						'install-plugin_' . $slug
					);
					break;
				case 'deactivate':
					$action_url = add_query_arg(
						array(
							'action'        => 'deactivate',
							'plugin'        => rawurlencode( $file_path ),
							'plugin_status' => 'all',
							'paged'         => '1',
							'_wpnonce'      => wp_create_nonce( 'deactivate-plugin_' . $file_path ),
						), network_admin_url( 'plugins.php' )
					);
					break;
				case 'activate':
					$action_url = add_query_arg(
						array(
							'action'        => 'activate',
							'plugin'        => rawurlencode( $file_path ),
							'plugin_status' => 'all',
							'paged'         => '1',
							'_wpnonce'      => wp_create_nonce( 'activate-plugin_' . $file_path ),
						), network_admin_url( 'plugins.php' )
					);
					break;
			} // End switch().

			return esc_url_raw( $action_url );
		}

		/**
		 * Callback for AJAX dismiss recommended action.
		 *
		 * @since 1.0.0
		 */
		public function dismiss_recommended_action_callback() {

			$todo      = ( isset( $_GET['todo'] ) ) ? esc_attr( wp_unslash( $_GET['todo'] ) ) : '';
			$action_id = ( isset( $_GET['id'] ) ) ? esc_attr( wp_unslash( $_GET['id'] ) ) : '';
			$wpnonce   = ( isset( $_GET['_wpnonce'] ) ) ? esc_attr( wp_unslash( $_GET['_wpnonce'] ) ) : '';

			$nonce = 'action-' . $action_id . '-' . $todo;

			if ( false === wp_verify_nonce( $wpnonce, $nonce ) ) {
				wp_die();
			}

			$action_detail = array();

			$recommended_actions = isset( $this->config['recommended_actions'] ) ? $this->config['recommended_actions'] : array();
			if ( ! empty( $recommended_actions ) ) {
				foreach ( $recommended_actions['content'] as $action ) {
					$action_detail[ $action['id'] ] = true;
				}
			}

			$options = get_option( $this->action_key );
			if ( $options ) {
				$action_detail = array_merge( $action_detail, $options );
			}

			switch ( $todo ) {
				case 'add':
					$action_detail[ $action_id ] = true;
					break;

				case 'dismiss':
					$action_detail[ $action_id ] = false;
					break;

				default:
					break;
			}

			update_option( $this->action_key, $action_detail );

			wp_die();
		}

		/**
		 * Helper function to extract the file path of the plugin file from the
		 * plugin slug, if the plugin is installed.
		 *
		 * @since 1.0.0
		 *
		 * @param string $slug Plugin slug (typically folder name).
		 * @return string Either file path for plugin if installed, or just the plugin slug.
		 */
		private function get_plugin_basename_from_slug( $slug ) {
			$keys = array_keys( $this->get_plugins() );

			foreach ( $keys as $key ) {
				if ( preg_match( '|^' . $slug . '/|', $key ) ) {
					return $key;
				}
			}

			return $slug;
		}

		/**
		 * Wrapper around the core WP get_plugins function, making sure it's actually available.
		 *
		 * @since 1.0.0
		 *
		 * @param string $plugin_folder Optional. Relative path to single plugin folder.
		 * @return array Array of installed plugins with plugin information.
		 */
		public function get_plugins( $plugin_folder = '' ) {
			if ( ! function_exists( 'get_plugins' ) ) {
				require_once ABSPATH . 'wp-admin/includes/plugin.php';
			}

			return get_plugins( $plugin_folder );
		}

		/**
		 * Check if a plugin is installed.
		 *
		 * @since 1.0.0
		 *
		 * @param string $slug Plugin slug.
		 * @return bool True if installed, false otherwise.
		 */
		private function is_plugin_installed( $slug ) {
			$installed_plugins = $this->get_plugins(); // Retrieve a list of all installed plugins (WP cached).

			$file_path = $this->get_plugin_basename_from_slug( $slug );

			return ( ! empty( $installed_plugins[ $file_path ] ) );
		}

		/**
		 * Check if a plugin is active.
		 *
		 * @since 1.0.0
		 *
		 * @param string $slug Plugin slug.
		 * @return bool True if active, false otherwise.
		 */
		private function is_plugin_active( $slug ) {
			$file_path = $this->get_plugin_basename_from_slug( $slug );

			if ( ! function_exists( 'is_plugin_active' ) ) {
				require_once ABSPATH . 'wp-admin/includes/plugin.php';
			}

			return is_plugin_active( $file_path );
		}

	}
} // End if().
