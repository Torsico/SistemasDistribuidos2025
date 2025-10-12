require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'usuarios_pb'
require 'usuarios_services_pb'
require 'rol_pb'
require 'rol_services_pb'
require 'eventos_pb'
require 'eventos_services_pb'
require 'donaciones_pb'
require 'donaciones_services_pb'
require 'time'
require 'google/protobuf/empty_pb'
require 'google/protobuf/well_known_types'

class EventosController < ApplicationController
	
	@@stub = nil
	@@stubuser = nil
	@@stubdon = nil
	
	before_action do
		unless @@stub # reusar stub en vez de crear uno nuevo
			@@stub = Eventos::EventosService::Stub.new('localhost:50051', :this_channel_is_insecure)
			@@stubdon = Donaciones::DonacionesService::Stub.new('localhost:50051', :this_channel_is_insecure)
			@@stubuser = Usuarios::UsuarioService::Stub.new('localhost:50051', :this_channel_is_insecure)
		end
		
		@alldons = @@stubdon.get_donaciones(Google::Protobuf::Empty.new).donaciones
		@allusers = @@stubuser.get_usuarios(Google::Protobuf::Empty.new).usuarios
		
		@donLUT = {}
		@alldons.each do |don|
			id = don.iddonaciones
			@donLUT[id] = don
		end
		@userLUT = {}
		@allusers.each do |u|
			id = u.idusuario
			@userLUT[id] = u
		end
		
		@allevs = @@stub.get_eventos(Google::Protobuf::Empty.new).evento
		
		# HORRIBLE HACK POR DESESPERACION, NO HACER ESTO EN CASA
		todos = {}
		@allevs.each do |item|
			todos[item.ideventos] = item
		end
		@@lasttodos = todos
	end
	
	def index
		
		todos = {}
		
		begin
			@badlist = false
			
			rp = @@stub.get_eventos(Google::Protobuf::Empty.new)
			
			rp.evento.each do |item|
				todos[item.ideventos] = item
			end
			
			todouser = {}
			rpu = @@stubuser.get_usuarios(Google::Protobuf::Empty.new)
			rpu.usuarios.each do |user|
				u = Usuario.new(user)
				todouser[u.idusuario] = u
			end
			
			@users = todouser
			
		rescue GRPC::Unavailable => exception
			@badlist = true
			
			flash[:noticecolor] = @@color_error
			flash[:noticetext] = "503: El servidor no esta disponible"
		rescue => exception
			@badlist = true
			
			puts exception
			flash[:noticecolor] = @@color_supererror
			flash[:noticetext] = exception
		end
		
		@items = todos
		@@lasttodos = todos
	end
	
	def altaform
		@style = :alta
		form
	end
	def modform
		@style = :mod
		@id = params[:id]
		form
	end
	def bajaform
		@style = :baja
		@id = params[:id]
		form
	end
	
	def form
		# TODO BUG: El listado de donaciones no se actualiza al regresar a la pagina.
		# Esto es por el uso del cache @@lasttodos para economizar en uso de red
		# Aunque no hace falta hacer tanto asi...
		#flash[:noticetext] = "make? '#{@make}' id? '#{@id}' gog? #{@@lasttodos}"
		#flash[:noticetext] = "!!!"
		if @style == :alta
		else
			@editee = @@lasttodos[@id.to_i]
			
			#p "ABBBBBBBBBBAAAAAAAAAAAAA"
			#p @editee
			#p @donLUT
			#@userlist
			# TODO lista de usuarios para asignar participacion
			# TODO lista de donaciones para... donar
		end
		
		render :form
	end
	
	# assign item field
	# no me gusta asignar algo y despues llamar clear (dos lineas al pepe), asi que...
	# (esto iria mejor en un importable, estilo "utils.rb")
	def aif_string(item, field, value)
		if value.nil? || value == ""
			item.public_send("clear_#{field}")
		else
			item.public_send("#{field}=", value)
		end
	end
	def aif_number(item, field, value)
		if value.nil? || value == 0
			item.public_send("clear_#{field}")
		else
			item.public_send("#{field}=", value)
		end
	end
	def aif_bool(item, field, value)
		if value.nil?
			item.public_send("clear_#{field}")
		else
			value = !!value # cast, por si acaso
			item.public_send("#{field}=", value)
		end
	end
	def aif_any(item, field, value)
		if value.nil?
			item.public_send("clear_#{field}")
		else
			item.public_send("#{field}=", value)
		end
	end
	
	def grpc_item_from_params(writealta)
		d = Eventos::Eventos.new
		
		aif_number(d, :ideventos, params[:ideventos]&.to_i || params[:id]&.to_i)
		aif_string(d, :nombre, params[:nombre])
		aif_string(d, :descripcion, params[:descripcion])
		
		aif_any(d, :fechaHora,
			Google::Protobuf::Timestamp.from_time(
				Time.parse(
					params[:fechaHora]
				)
			)
		)
		
		#aif_timestamp(d, :fechaHora, params[:fechaHora])
		#repeated usuarios
		#repeated donarevento? talvez?
		
		return d
	end
	
	def altapost
		flash[:noticetext] = "egento"
		flash[:noticecolor] = @@color_success
		
		ev = grpc_item_from_params(true)
		
		rq = Eventos::AltaEventoRequest.new
		rq.evento = ev
		
		metadata = { "authorization" => $session.token }
		
		begin
			rp = @@stub.alta_evento(rq, metadata: metadata)
			
			if rp.suceso then
			flash[:noticetext] = "Evento \"#{params[:nombre]}\" creado!"
			flash[:noticecolor] = @@color_success
			else
				flash[:noticetext] = "Error desconocido"
				flash[:noticecolor] = @@color_error
			end
			
			redirect_to "/eventos"
			
		rescue => exception # no puedo capturar GRPC::Unknown
			flash[:noticetext] = "No se pudo crear el evento.\n\n#{exception}"
			flash[:noticecolor] = @@color_success
			redirect_to "/eventos/alta"
		end
	end
	def modpost
		ev = grpc_item_from_params(false)
		
		rq = Eventos::ModEventoRequest.new
		rq.evento = ev
		
		metadata = { "authorization" => $session.token }
		rp = @@stub.mod_evento(rq, metadata: metadata)
		
		if rp.suceso then
			flash[:noticetext] = "Evento \"#{params[:nombre]}\" modificado!"
			flash[:noticecolor] = @@color_success
			redirect_to "/eventos"
		else
			flash[:noticetext] = "Error desconocido"
			flash[:noticecolor] = @@color_error
			redirect_to "/eventos/mod/#{params[:id]}"
		end
	end
	
	def joinpost
		rq = Eventos::ModificarMiembroRequest.new
		ue = Eventos::UsuarioEvento.new
		rq.miembro = ue
		
		# no usamos aif por que SABEMOS que esto no sera nil
		ue.idevento = params[:id].to_i
		ue.idusuario = params[:userid].to_i || $session.user.idusuario # nil? capaz es el modo voluntario
		
		metadata = { "authorization" => $session.token }
		
		eventUsers = @@lasttodos[ue.idevento].usuario
		chosenUser = @userLUT[ue.idusuario]
		isUserJoining = !eventUsers.include?(chosenUser)
		
		begin
			rp = nil
			if isUserJoining then
				rp = @@stub.asignar_miembro(rq, metadata: metadata)
				flash[:noticetext] = "Usuario #{chosenUser.nombreUsuario} ahora es miembro del evento!"
			else
				rp = @@stub.quitar_miembro(rq, metadata: metadata)
				flash[:noticetext] = "Usuario #{chosenUser.nombreUsuario} ya no participa en el evento."
			end
			flash[:noticecolor] = @@color_success
		rescue GRPC::BadStatus => exception
			p exception
			flash[:noticetext] = "Excepcion del lado remoto: #{exception.details}"
			flash[:noticecolor] = @@color_error
		rescue => exception
			p exception
			flash[:noticetext] = "Excepcion??? #{exception}"
			flash[:noticecolor] = @@color_supererror
		end
		
		redirect_to "/eventos/mod/#{params[:id]}"
	end
	
	def donatepost
		rq = Eventos::DonarRequest.new
		rqd = Eventos::DonarEvento.new
		rq.donar = rqd
		
		# no usamos aif por que SABEMOS que esto no sera nil
		rqd.ideventos = params[:id].to_i
		rqd.iddonaciones = params[:itemid].to_i
		rqd.cantidad_donada = params[:cantidad].to_i
		
		metadata = { "authorization" => $session.token }
		
		begin
			rp = @@stub.donar_evento(rq, metadata: metadata)
			flash[:noticetext] = "Donacion hecha con exito!"
			flash[:noticecolor] = @@color_success
		rescue => exception
			p exception
			#flash[:noticetext] = "Excepcion:\n#{exception}"
			flash[:noticetext] = "Excepcion del lado remoto: #{exception.details}"
			flash[:noticecolor] = @@color_error
		end
		
		redirect_to "/eventos/mod/#{params[:id]}"
		#render plain: "donate ok?\n\n#{rq}\n\n#{rqd}\n\n#{rp}\n\n"
	end
	
	def bajapost
		rq = Eventos::BajaEventoRequest.new
		rq.ideventos = params[:id]&.to_i
		
		metadata = { "authorization" => $session.token }
		rp = @@stub.baja_evento(rq, metadata: metadata)
		
		if rp.suceso then
			flash[:noticetext] = "Evento dado de baja."
			flash[:noticecolor] = @@color_success
			redirect_to "/eventos"
		else
			flash[:noticetext] = "Error desconocido"
			flash[:noticecolor] = @@color_error
			redirect_to "/eventos/baja/#{params[:id]}"
		end
	end
	
end
  