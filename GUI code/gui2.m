function varargout = gui2(varargin)
% GUI2 MATLAB code for gui2.fig
%      GUI2, by itself, creates a new GUI2 or raises the existing
%      singleton*.
%
%      H = GUI2 returns the handle to a new GUI2 or the handle to
%      the existing singleton*.
%
%      GUI2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI2.M with the given input arguments.
%
%      GUI2('Property','Value',...) creates a new GUI2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before gui2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to gui2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help gui2

% Last Modified by GUIDE v2.5 22-Feb-2023 11:49:39

global buttonresponse

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @gui2_OpeningFcn, ...
    'gui_OutputFcn',  @gui2_OutputFcn, ...
    'gui_LayoutFcn',  [] , ...
    'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before gui2 is made visible.
function gui2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to gui2 (see VARARGIN)
global buttonresponse
%set(handles.figure1,'Position',get(0,'ScreenSize'))

% UIWAIT makes gui2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);
handles.guiState = varargin{1};
infoText = varargin{2};
buttonText = varargin{3};
actionButtonText = varargin{4};
title_text = varargin{5};
%curr_col = varargin{6};
exitbuttontext = varargin{6};
handles.output = hObject;
guidata(hObject,handles);
%handles.response = strings(1,5);
disp(handles.guiState)
switch handles.guiState
    case 'open'
        set(handles.actionButton,'String',actionButtonText,'Visible','on')
        set(handles.ExitButton,'String',exitbuttontext,'Visible','on')
        set(handles.infoText,'String',infoText)
        set(handles.buttonPanel,'Visible','off')
    case 'info'
        set(handles.actionButton,'String',actionButtonText,'Visible','on')
        set(handles.ExitButton,'String',exitbuttontext,'Visible','on')
        set(handles.infoText,'String',infoText)
        set(handles.buttonPanel,'Visible','on')
        uiwait(handles.figure1)
    case 'trial'
        set(handles.actionButton,'String',actionButtonText,'Visible','on')
        set(handles.ExitButton,'String',exitbuttontext,'Visible','on')
        set(handles.infoText,'String',infoText)
        set(handles.buttonPanel,'Visible','on')
    case 'response'
        %buttonresponse =strings(1,5);
        set(handles.actionButton,'String',actionButtonText,'Visible','on')
        set(handles.ExitButton,'String',exitbuttontext,'Visible','on')
        set(handles.infoText,'String',infoText,'Position',[5.285714285714286,0.588235294117647,10000,9.117647058823529])
        set(handles.buttonPanel,'Visible','on')
        for ncat = 1:length(buttonText(1,:))
            for nButton = 1:length(buttonText(:,1))
                %if ncat == curr_col
                eval(['set(handles.b',num2str(ncat),num2str(nButton),',''String'',buttonText{nButton, ncat},''Visible'',''on'',''Enable'',''on'')'])
                %else
                %    eval(['set(handles.b',num2str(ncat),num2str(nButton),',''String'',buttonText{nButton, ncat},''Visible'',''on'',''Enable'',''off'')'])
                %end
            end
        end
        uiwait(handles.figure1)
    case 'exit'
        set(handles.actionButton,'String',actionButtonText,'Visible','on')
        set(handles.ExitButton,'String',exitbuttontext,'Visible','on')
        set(handles.infoText,'String',infoText)
        set(handles.buttonPanel,'Visible','on')
        uiwait(handles.figure1)
end





% --- Outputs from this function are returned to the command line.
function varargout = gui2_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global buttonresponse
set(handles.figure1, 'units','normalized','outerposition',[0 0 1 1]);
% Get default command line output from handles structure
switch handles.guiState
    case 'response'
        varargout{1} = buttonresponse;
        delete(handles.figure1)
    case 'open'
        varargout{1} = handles.output;
    case 'close'
        delete(handles.figure1);
    case 'info'
        varargout{1} = handles.output;
    case 'exit'
        varargout{1} = handles.output;

end

% --- Executes on button press in actionButton.
function actionButton_Callback(hObject, eventdata, handles)
%hObject    handle to actionButton (see GCBO)
%eventdata  reserved - to be defined in a future version of MATLAB
%handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1)
    case 'response'
        handles.response = buttonresponse;
        guidata(hObject,handles);
        uiresume(handles.figure1)
       % delete(handles.figure1) % CLOSES PROGRAM
end



% --- Executes on button press in actionButton.
%function actionButton_Callback(hObject, eventdata, handles)
% hObject    handle to actionButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%switch handles.guiState
%  case 'info'
%uiresume(handles.figure1)
% case 'exit'
%    handles.output = get(hObject,'String');
%  uiresume(handles.figure1)
%end


% --- Executes on button press in b11.
function b11_Callback(hObject, eventdata, handles)
% hObject    handle to b11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1)= get(hObject,'String');
        guidata(hObject,handles);
        %uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b12.
function b12_Callback(hObject, eventdata, handles)
% hObject    handle to b12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1)= get(hObject,'String');
        guidata(hObject,handles);
        %uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b13.
function b13_Callback(hObject, eventdata, handles)
% hObject    handle to b13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b14.
function b14_Callback(hObject, eventdata, handles)
% hObject    handle to b14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        %uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b15.
function b15_Callback(hObject, eventdata, handles)
% hObject    handle to b15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b16.
function b16_Callback(hObject, eventdata, handles)
% hObject    handle to b16 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b17.
function b17_Callback(hObject, eventdata, handles)
% hObject    handle to b17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b18.
function b18_Callback(hObject, eventdata, handles)
% hObject    handle to b18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b19.
function b19_Callback(hObject, eventdata, handles)
% hObject    handle to b19 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in b110.
function b110_Callback(hObject, eventdata, handles)
% hObject    handle to b110 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(1)= string(get(hObject,'String'));
        %handles.response(1) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton21.
function b21_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton22.
function b22_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        % handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton23.
function b23_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton23 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton24.
function b24_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton25.
function b25_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton25 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton26.
function b26_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton27.
function b27_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton27 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton28.
function b28_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton28 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in b29.
function b29_Callback(hObject, eventdata, handles)
% hObject    handle to b29 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        % handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b210.
function b210_Callback(hObject, eventdata, handles)
% hObject    handle to b210 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(2)= string(get(hObject,'String'));
        %handles.response(2) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end




% --- Executes on button press in pushbutton31.
function b31_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton31 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        %handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton32.
function b32_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton32 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        % handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton33.
function b33_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton33 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        %handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton34.
function b34_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton34 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        %handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton35.
function b35_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton35 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        % handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton36.
function b36_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton36 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        %handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton37.
function b37_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton37 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)=string(get(hObject,'String'));
        % handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton38.
function b38_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton38 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        %handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
% --- Executes on button press in b39.
function b39_Callback(hObject, eventdata, handles)
% hObject    handle to b39 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        % handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b310.
function b310_Callback(hObject, eventdata, handles)
% hObject    handle to b310 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(3)= string(get(hObject,'String'));
        %handles.response(3) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end








% --- Executes on button press in pushbutton41.
function b41_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton41 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        % handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton42.
function b42_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton42 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton43.
function b43_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton43 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in pushbutton44.
function b44_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
% --- Executes on button press in pushbutton44.
function b45_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
% --- Executes on button press in pushbutton44.
function b46_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
% --- Executes on button press in pushbutton44.
function b47_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
% --- Executes on button press in pushbutton44.
function b48_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton44 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
       set(handles.infoText,'String',buttonresponse)
end



% --- Executes on button press in b49.
function b49_Callback(hObject, eventdata, handles)
% hObject    handle to b49 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        %handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b410.
function b410_Callback(hObject, eventdata, handles)
% hObject    handle to b410 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(4)= string(get(hObject,'String'));
        % handles.response(4) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
% --- Executes on button press in pushbutton51.
function b51_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton51 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in pushbutton52.
function b52_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton52 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in pushbutton53.
function b53_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton53 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        % handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end






% --- Executes on button press in b54.
function b54_Callback(hObject, eventdata, handles)
% hObject    handle to b54 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in b55.
function b55_Callback(hObject, eventdata, handles)
% hObject    handle to b55 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end


% --- Executes on button press in b56.
function b56_Callback(hObject, eventdata, handles)
% hObject    handle to b56 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse


switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b57.
function b57_Callback(hObject, eventdata, handles)
% hObject    handle to b57 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        % handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        %  uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end



% --- Executes on button press in b58.
function b58_Callback(hObject, eventdata, handles)
% hObject    handle to b58 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        % handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b59.
function b59_Callback(hObject, eventdata, handles)
% hObject    handle to b59 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end

% --- Executes on button press in b510.
function b510_Callback(hObject, eventdata, handles)
% hObject    handle to b510 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1);
    case 'response'
        buttonresponse(5)= string(get(hObject,'String'));
        %handles.response(5) = get(hObject,'String');
        guidata(hObject,handles);
        % uiresume(handles.figure1)
        set(handles.infoText,'String',buttonresponse)
end
%S--- Executes on button press in ExitButton.
function ExitButton_Callback(hObject, eventdata, handles)
%hObject    handle to ExitButton (see GCBO)
%eventdata  reserved - to be defined in a future version of MATLAB
%handles    structure with handles and user data (see GUIDATA)
global buttonresponse

switch handles.guiState
    case 'info'
        uiresume(handles.figure1)
    case 'exit'
        handles.output = get(hObject,'String');
        guidata(hObject,handles);
        delete(handles.figure1)
end
