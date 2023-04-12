function varargout = Instruction(varargin)
% INSTRUCTION MATLAB code for Instruction.fig
%      INSTRUCTION, by itself, creates a new INSTRUCTION or raises the existing
%      singleton*.
%
%      H = INSTRUCTION returns the handle to a new INSTRUCTION or the handle to
%      the existing singleton*.
%
%      INSTRUCTION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in INSTRUCTION.M with the given input arguments.
%
%      INSTRUCTION('Property','Value',...) creates a new INSTRUCTION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Instruction_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Instruction_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Instruction

% Last Modified by GUIDE v2.5 20-Mar-2023 18:45:13

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
    'gui_Singleton',  gui_Singleton, ...
    'gui_OpeningFcn', @Instruction_OpeningFcn, ...
    'gui_OutputFcn',  @Instruction_OutputFcn, ...
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


% --- Executes just before Instruction is made visible.
function Instruction_OpeningFcn(hObject, ~, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Instruction (see VARARGIN)

global release
release = false;
% UIWAIT makes Instruction wait for user response (see UIRESUME)
%uiwait(handles.figure1);


     
infoText = varargin{1};
actionButtonText = varargin{2};


handles.output = hObject;
guidata(hObject,handles);




 set(handles.actionButton,'String',actionButtonText,'Visible','on')
 set(handles.infoText,'String',infoText)
       
  


% --- Outputs from this function are returned to the command line.
function varargout = Instruction_OutputFcn(hObject, eventdata, handles)
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

        varargout{1} = handles.output;
   


% --- Executes on button press in actionButton.
function actionButton_Callback(hObject, eventdata, handles)
%hObject    handle to actionButton (see GCBO)
%eventdata  reserved - to be defined in a future version of MATLAB
%handles    structure with handles and user data (see GUIDATA)
global release
release = true;
delete(handles.figure1)


