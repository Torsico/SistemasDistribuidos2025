require 'clases' # no es necesario gracias a Rails, pero permite recargar

class UsuariosController < ApplicationController
    
    def root
        lista = []
        lista.push Usuario.new.scramble!
        lista.push Usuario.new.scramble!
        lista.push Usuario.new.scramble!
        
        @usuarios = lista
    end
end
  