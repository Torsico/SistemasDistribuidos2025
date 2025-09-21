class ApplicationController < ActionController::Base
  # Only allow modern browsers supporting webp images, web push, badges, import maps, CSS nesting, and CSS :has.
  allow_browser versions: :modern
  
  skip_before_action :verify_authenticity_token
  
  @@color_info = "#94c2ff" # un azulcito amigable
  @@color_success = "#8aff88" # un verde
  @@color_error = "#f88" # un rojo no tan fuerte
  @@color_supererror = "#f00" # rojo vivo
  
  before_action :notice_setup
  
  # prepara la cajita de notificacion
  def notice_setup
    #flash[:noticetext] = nil # si recibe texto, shared/notif se mostrara
    #flash[:noticecolor] = @@color_info
  end
end
