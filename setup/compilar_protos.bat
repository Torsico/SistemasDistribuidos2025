:: grpc_tools_ruby_protoc -I ../../protos --ruby_out=../lib --grpc_out=../lib ../../protos/route_guide.proto
:: grpc_tools_ruby_protoc -I proto --ruby_out=../cliente/lib --grpc_out=../cliente/lib protos/cosas.proto
::start "titulo" grpc_tools_ruby_protoc -I proto --ruby_out=../cliente/lib --grpc_out=../cliente/lib
:: grpc_tools_ruby_protoc      -Iproto --ruby_out=../cliente/lib --grpc_out=../cliente/lib
:: python -m grpc_tools.protoc -Iproto --ruby_out=../servidor/lib --grpc_out=../cliente/lib
@echo off

:: .. es el root del proyecto
set rubyTarget=..\cliente\lib
set pyTarget=..\servidor\proto
set compFiles=rol.proto usuarios.proto eventos.proto donaciones.proto session.proto

echo.
echo Compilando protos Ruby...
call grpc_tools_ruby_protoc ^
	-Iproto ^
	--ruby_out=%rubyTarget% ^
	--grpc_out=%rubyTarget% ^
	%compFiles%


echo.
echo Compilando protos Python...
python -m grpc_tools.protoc ^
	-Iproto ^
	--python_out=%pyTarget% ^
	--pyi_out=%pyTarget% ^
	--grpc_python_out=%pyTarget% ^
	%compFiles%

echo.
echo Listo!
timeout /T 3