DT = 1;
N = 5702;
b1 = input('b1');
b2 = input('b2');
b3 = input('b3');
s_e = input('s_e');
s_u = input('s_u');
s_v = input('s_v');
q_1_array = zeros(1,N);
q_2_array = zeros(1,N);
q_3_array = zeros(1,N);
q_4_array = zeros(1,N);
a1 = q1(1,1);
a2 = q2(1,1);
a3 = q3(1,1);
a4 = q4(1,1);
q_next = [a1,a2,a3,a4];
time = 1:1:N;
m_P = eye(6);
m_Q = 0.25*[(s_e^2+s_v^2*DT+(1/3)*s_u^2*DT*DT*DT)*eye(3) (s_u^2*DT*DT)*eye(3);(s_u^2*DT*DT)*eye(3) (4*s_u^2*DT)*eye(3)]; 
m_G = [-0.5*eye(3) zeros(3);zeros(3) eye(3)];
m_R = 0.05*eye(3);
m_H = [eye(3) zeros(3)];
v_de_X = zeros(6,1);
digits(6)


for i=1:1:N
quat_1 = q1(i,1);
quat_2 = q2(i,1);
quat_3 = q3(i,1);
quat_4 = q4(i,1); %quat_4 is the scalar part and quat_1 to quat_3 are vector part
q_y = [quat_1 quat_2 quat_3 quat_4];
w1 = vpa(wxdegsec(i,1));
w2 = vpa(wydegsec(i,1));
w3 = vpa(wzdegsec(i,1));
v_b = [b1;b2;b3];
v_w = [w1;w2;w3];
m_wx = [0,-w3,w2;w3,0,-w1;-w2,w1,0];
v_X = [quat_1;quat_2;quat_3;quat_4;b1;b2;b3];   
k_s = sin(0.5*norm(v_w)*DT); 
k_c = cos(0.5*norm(v_w)*DT);
q_prev = q_next;

%defining the F matrix
m_F = [m_wx -0.5*eye(3);zeros(3) zeros(3)];
m_tau = (eye(6) + 0.5*DT*DT*m_F + (1/6)*DT*DT*DT*m_F*m_F)*m_G;
v_psi = k_s*v_w/norm(v_w);
m_psiX = [0 -v_psi(3) v_psi(2);v_psi(3) 0 -v_psi(1);-v_psi(2) v_psi(1) 0];
m_omega = [k_c*eye(3)-m_psiX v_psi;-v_psi.' k_c];
m_phi = eye(6) + m_F*DT + 0.5*DT*DT*m_F;
m_phi_tilda = [m_omega zeros([4,3]);zeros([3,4]) eye(3)];
  

%predict
v_X = m_phi_tilda*v_X;
m_P = m_phi*m_P*m_phi.' + m_Q;

%measurement update 
q_prev = m_omega*q_prev.';
v_del_q = quatmultiply(quatconj(q_prev.'),q_y);
v_del_qk = [real(v_del_q(1)) real(v_del_q(2)) real(v_del_q(3)) real(sqrt(1-(v_del_q(1)^2 + v_del_q(2)^2 + v_del_q(3)^2)))];
q_next = quatmultiply(q_prev.',v_del_qk);
q_next = q_next/norm(q_next);
q_1_array(i) = q_next(1);
q_2_array(i) = q_next(2);
q_3_array(i) = q_next(3);
q_4_array(i) = q_next(4);
m_S = m_H*m_P*m_H.' + m_R;
m_K = m_P*m_H.'/m_S;
m_P = (eye(6) - m_K*m_H)*m_P;
end

q1_test = zeros(1,N);
for j=1:1:N
q1_test(j) = q1(j,1);
end
plot(time,q_1_array)
hold on
plot(time,q1_test)




             





                    
                 
                 

