class UsuariosController < ApplicationController
    def root
        puts "texto"
        render json: [ "texto" ]
    end
end
  