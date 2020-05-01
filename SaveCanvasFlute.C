#include <iostream>
#include "TCanvas.h"
#include "TFile.h"
#include "TString.h"
#include "MStatusArray.h"

using namespace std;

void SaveCanvasFlute(TString path){
  cout << path << endl;
  TFile * f = TFile::Open(path);
  f->ls();
  MStatusArray * status_array = f->Get("MStatusDisplay");

  //Cuts
  TCanvas * can_Cuts = static_cast<TCanvas*>(status_array->FindCanvas("Cuts"));
  can_Cuts->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_Cuts = path;
  png_name_Cuts.ReplaceAll(".root", "_Cuts.pdf");
  can_Cuts->SaveAs(png_name_Cuts);
  png_name_Cuts.ReplaceAll(".pdf", ".png");
  can_Cuts->SaveAs(png_name_Cuts);

  //CollArea
  TCanvas * can_CollAreaEest = static_cast<TCanvas*>(status_array->FindCanvas("Coll. Area Eest"));
  can_CollAreaEest->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_CollAreaEest = path;
  png_name_CollAreaEest.ReplaceAll(".root", "_CollAreaEest.pdf");
  can_CollAreaEest->SaveAs(png_name_CollAreaEest);
  png_name_CollAreaEest.ReplaceAll(".pdf", ".png");
  can_CollAreaEest->SaveAs(png_name_CollAreaEest);

  //Excess
  TCanvas * can_Excess = static_cast<TCanvas*>(status_array->FindCanvas("Excess vs. Eest"));
  can_Excess->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_Excess = path;
  png_name_Excess.ReplaceAll(".root", "_Excess.pdf");
  can_Excess->SaveAs(png_name_Excess);
  png_name_Excess.ReplaceAll(".pdf", ".png");
  can_Excess->SaveAs(png_name_Excess);

  //Bkg
  TCanvas * can_Background = static_cast<TCanvas*>(status_array->FindCanvas("Background vs. Eest"));
  can_Background->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_Background = path;
  png_name_Background.ReplaceAll(".root", "_Background.pdf");
  can_Background->SaveAs(png_name_Background);
  png_name_Background.ReplaceAll(".pdf", ".png");
  can_Background->SaveAs(png_name_Background);

  //SED
  TCanvas * can_SED = static_cast<TCanvas*>(status_array->FindCanvas("SED"));
  can_SED->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_SED = path;
  png_name_SED.ReplaceAll(".root", "_SED.pdf");
  can_SED->SaveAs(png_name_SED);
  png_name_SED.ReplaceAll(".pdf", ".png");
  can_SED->SaveAs(png_name_SED);

  //LC
  TCanvas * can_Light = static_cast<TCanvas*>(status_array->FindCanvas("Light Curve"));
  can_Light->Draw();
  gPad->Update();
  gPad->Modified();
  TString png_name_Light = path;
  png_name_Light.ReplaceAll(".root", "_LightCurve.pdf");
  can_Light->SaveAs(png_name_Light);
  png_name_Light.ReplaceAll(".pdf", ".png");
  can_Light->SaveAs(png_name_Light);

  f->Close();
  delete f;
  delete status_array;
  delete can_Cuts;
  delete can_CollAreaEest;
  delete can_Excess;
  delete can_Background;
  delete can_SED;
  delete can_Light;
  return;
}


int main(int argc, char * argv[]){
  SaveCanvasFlute(argv[1]);
  return 1;
}
