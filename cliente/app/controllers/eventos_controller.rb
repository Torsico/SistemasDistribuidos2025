require 'clases' # no es necesario gracias a Rails, pero permite recargar

require 'grpc'
require 'google/protobuf/empty_pb'

class EventosController < ApplicationController
    
    @@stub = nil
    
    before_action do
        unless @@stub # reusar stub en vez de crear uno nuevo
            #@@stub = Session::LoginService::Stub.new('localhost:50051', :this_channel_is_insecure)
        end
    end
    
    def index
        # cosas
        # flash[:noticetext] = ":)"
        # flash[:noticecolor] = @@color_info
    end
end
  