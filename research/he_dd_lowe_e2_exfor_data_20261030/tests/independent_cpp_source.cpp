#include <boost/multiprecision/cpp_dec_float.hpp>
#include <fstream>
#include <sstream>
#include <iostream>
#include <array>
#include <string>
#include <map>
#include <set>
#include <stdexcept>
using H=boost::multiprecision::cpp_dec_float_100;

int main(int argc,char**argv) {
  if(argc!=2)throw std::runtime_error("Pass source directory");
  const std::map<std::string,std::string> paths = {
    {"M0011","M0011.x4"},{"M0826","M0826.x4"},{"M0034","M0034.x4"},{"M0475","M0475.x4"}};
  const std::map<std::string,int> expected={
    {"M0011002",14},{"M0011003",7},{"M0826002",4},{"M0826003",9},
    {"M0034005",14},{"M0034006",9},{"M0475002",12},{"M0475003",6}};
  const H M("3727.3794118"), m("1875.61294500"), Q=2*m-M;
  const H E_thr=((2*m)*(2*m)-M*M)/(2*M);
  if(abs(Q-H("23.8464782"))>H("1e-85")||abs(E_thr-Q-Q*Q/(2*M))>H("1e-85"))throw std::runtime_error("bad threshold identity");
  std::map<std::string,int> n;std::map<int,H> tot,e2;
  for(auto &[entry,file]:paths){
    std::ifstream in(std::string(argv[1])+"/"+file);if(!in)throw std::runtime_error("source open");
    std::string line,sub;int datalines=0,columns=0,skips=0;
    while(std::getline(in,line)) {
      if(line.rfind("SUBENT",0)==0){std::istringstream ls(line);std::string key;ls>>key>>sub;}
      if(line.rfind("DATA ",0)==0){
         std::istringstream ls(line);std::string key;ls>>key>>columns>>datalines;skips=2;
         continue;
      }
      if(skips>0){skips--;continue;}
      if(datalines<=0)continue;
      datalines--;
      if(expected.find(sub)==expected.end())continue; // no proton/neutron contamination
      std::istringstream ls(line);std::string cols[4];
      for(int j=0;j<columns;j++) { if(!(ls>>cols[j])) throw std::runtime_error("bad source row"); }
      n[sub]++;
      H en(cols[0]),sig(cols[columns-2]),err(cols[columns-1]);
      if(sig<0||err<0)throw std::runtime_error("negative source data");
      if(sub=="M0011002"||sub=="M0011003"){
         if(en<E_thr)throw std::runtime_error("threshold failed");
         int E=en.convert_to<int>();
         if(sub=="M0011002"){if(en==E)tot[E]=sig;}
         else {if(en!=E)throw std::runtime_error("E2 matched energy not integer");e2[E]=sig;}
      }
      if(sub=="M0826002"){
         H hi(cols[1]);
         if(hi<=en||en<E_thr)throw std::runtime_error("bad window");
         H min_K=en-Q,max_K=hi-Q;
         if(!(sig*min_K<=sig*max_K))throw std::runtime_error("window support positivity");
      }
      if(sub=="M0826003"){
         H angmax(cols[1]);
         if(!(en>=0&&en<angmax&&angmax<=180))throw std::runtime_error("bad angle window");
      }
    }
  }
  if(n!=expected)throw std::runtime_error("wrong row set/cardinality");
  if(e2.size()!=7||tot.size()<7)throw std::runtime_error("wrong E2/total count");
  for(auto &[E, val]:e2){if(!(val>=0&&val<=tot.at(E)))throw std::runtime_error("nonphysical nominal E2 component");}
  if(abs(e2.at(26)/tot.at(26)-H(83)/H(87))>H("1e-85"))throw std::runtime_error("E2 frac26 mismatch");
  if(abs(e2.at(32)/tot.at(32)-H(127)/H(511))>H("1e-85"))throw std::runtime_error("E2 frac32 mismatch");
  std::cout<<"CPP_PASS source entries=4 rows=";
  int total=0;for(auto &[k,v]:n)total+=v;std::cout<<total;
  std::cout<<" author_E2_pairs="<<e2.size()<<" E2fraction26="<<e2.at(26)/tot.at(26)<<" E2fraction32="<<e2.at(32)/tot.at(32) <<" Q="<<Q<<" Ethr="<<E_thr<<"\n";
}
