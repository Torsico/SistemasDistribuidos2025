Rails.application.routes.draw do
	# Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

	# Reveal health status on /up that returns 200 if the app boots with no exceptions, otherwise 500.
	# Can be used by load balancers and uptime monitors to verify that the app is live.
	get "up" => "rails/health#show", as: :rails_health_check

	# Render dynamic PWA files from app/views/pwa/* (remember to link manifest in application.html.erb)
	# get "manifest" => "rails/pwa#manifest", as: :pwa_manifest
	# get "service-worker" => "rails/pwa#service_worker", as: :pwa_service_worker

	# Defines the root path route ("/")
	# root "posts#index"

	root "root#root"
	
	#resources(...) enruta:
	# #index #new #show #edit (todos GET)
	# #create #update #destroy (POST PATCH/PUT DELETE)
	#resources :usuarios
	
	get "login"		=> "root#login"
	post "login"	=> "root#loginpost"
	post "logout"	=> "root#logoutpost"
	
	get "usuarios"			=> "usuarios#index"
	get "usuarios/alta"		=> "usuarios#altaform"
	get "usuarios/mod/:id"	=> "usuarios#modform"
	post "usuarios/alta"	=> "usuarios#altapost"
	post "usuarios/mod/:id"	=> "usuarios#modpost"
	
	get "inventarios"			=> "inventarios#index"
	get "inventario/alta"		=> "inventarios#altaform"
	get "inventario/mod/:id"	=> "inventarios#modform"
	get "inventario/baja/:id"	=> "inventarios#bajaform"
	post "inventario/alta"		=> "inventarios#altapost"
	post "inventario/mod/:id"	=> "inventarios#modpost"
	post "inventario/baja/:id"	=> "inventarios#bajapost"
	
	get "eventos"			=> "eventos#index"
	get "eventos/alta"		=> "eventos#altaform"
	get "eventos/mod/:id"	=> "eventos#modform"
	get "eventos/baja/:id"	=> "eventos#bajaform"
	post "eventos/alta"		=> "eventos#altapost"
	post "eventos/mod/:id"	=> "eventos#modpost"
	post "eventos/baja/:id"	=> "eventos#bajapost"
	
end
