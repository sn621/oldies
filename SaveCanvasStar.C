#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TString.h"
#include "MStatusArray.h"

using namespace std;

void SaveCanvasStar(TString path){
  cout << path << endl;
  TFile * f = TFile::Open(path);
  f->ls();
  MStatusArray * status_array = f->Get("MStatusDisplay");

  TCanvas * can_SurvPed = static_cast<TCanvas*>(status_array->FindCanvas("Surviving Pedestals"));
  can_SurvPed->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_SurvPed = path;
  png_name_SurvPed.ReplaceAll(".root", "_SurvPed.pdf");
  can_SurvPed->SaveAs(png_name_SurvPed);
  png_name_SurvPed.ReplaceAll(".pdf", ".png");
  can_SurvPed->SaveAs(png_name_SurvPed);

  f->Close();
  delete f;
  delete status_array;
  delete can_SurvPed;
  return;
}

int main(int argc, char * argv[]){
  SaveCanvasStar(argv[1]);
  return 1;
}
