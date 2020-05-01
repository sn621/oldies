#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TString.h"
#include "MStatusArray.h"

using namespace std;

void SaveCanvasOdie(TString path){
  cout << path << endl;
  TFile * f = TFile::Open(path);
  f->ls();
  MStatusArray * status_array = f->Get("MStatusDisplay");

  TCanvas* can_OnOffPlots = static_cast<TCanvas*>(status_array->FindCanvas("On-and-Off-Plots"));
  can_OnOffPlots->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_OnOffPlots = path;
  png_name_OnOffPlots.ReplaceAll(".root", "_OnOffPlots.pdf");
  can_OnOffPlots->SaveAs(png_name_OnOffPlots);
  png_name_OnOffPlots.ReplaceAll(".pdf", ".png");
  can_OnOffPlots->SaveAs(png_name_OnOffPlots);

  f->Close();
  delete f;
  delete status_array;
  delete can_OnOffPlots;
  return;
}

int main(int argc, char * argv[]){
  save_Cans_from_Odie(argv[1]);
  return 1;
}
